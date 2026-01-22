from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse
from typing import Optional
from app.services.template_parser import analyze_presentation
from app.services.slide_planner import generate_slide_plan
from app.services.ppt.ppt_exporter import generate_presentation
import logging

# Configure logger
logger = logging.getLogger("GenerateAPI")
logger.setLevel(logging.INFO)

router = APIRouter()

@router.post("/generate")
async def generate_ppt(
    text_input: str = Form(...),
    guidance: Optional[str] = Form(None),
    api_key: str = Form(...),
    file: UploadFile = File(...)
):
    if not api_key:
        raise HTTPException(status_code=400, detail="API Key is required")

    try:
        # Read and analyze template
        template_bytes = await file.read()
        
        # Analyze template to extract layouts, colors, fonts, and images
        logger.info("Analyzing template...")
        template_metadata = analyze_presentation(template_bytes)
        
        if template_metadata.get("error"):
            raise HTTPException(status_code=400, detail="Invalid PowerPoint template")
        
        # Generate Slide Plan using LLM
        logger.info("Generating slide plan with LLM...")
        try:
            plan = await generate_slide_plan(text_input, guidance, api_key)
        except Exception as e:
            logger.error(f"Slide Planning Failed: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to generate slide plan: {str(e)}")

        if not plan:
            raise HTTPException(status_code=500, detail="LLM returned empty plan")

        logger.info(f"Plan generated: {plan.get('meta', {}).get('slide_count', 0)} slides")

        # Generate PowerPoint with template metadata (images, colors, fonts)
        try:
            pptx_io = generate_presentation(template_bytes, plan, template_metadata)
        except Exception as e:
            logger.error(f"PPT Generation Failed: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to generate PPT: {str(e)}")
            
        return StreamingResponse(
            pptx_io,
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            headers={"Content-Disposition": "attachment; filename=generated_presentation.pptx"}
        )

    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Unexpected API Error: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
