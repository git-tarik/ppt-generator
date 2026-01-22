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
        # Phase 2: Read file content and analyze (Verification Step)
        template_bytes = await file.read()
        
        # We analyze just to log the structure (as per requirement to keep Phase 2 behavior)
        # and to ensure it's a valid PPT before proceeding.
        analyze_presentation(template_bytes) 
        
        # Phase 3: Generate Slide Plan (LLM)
        # Fail fast if this step fails (e.g., bad API key), as we no longer have a dummy fallback.
        try:
            plan = await generate_slide_plan(text_input, guidance, api_key)
        except Exception as e:
            logger.error(f"Slide Planning Failed: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to generate slide plan: {str(e)}")

        if not plan:
            raise HTTPException(status_code=500, detail="LLM returned empty plan")

        # Phase 4: Generate Real PPT
        try:
            pptx_io = generate_presentation(template_bytes, plan)
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
