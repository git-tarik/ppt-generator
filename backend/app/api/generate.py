from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse
from typing import Optional
from app.services.dummy_generator import generate_dummy_pptx
from app.services.template_parser import analyze_presentation

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
        # Phase 2: Read file content and analyze
        contents = await file.read()
        analyze_presentation(contents)
        
        # Reset file pointer if we were to use it again (though dummy generator doesn't use it)
        # await file.seek(0) 

        pptx_io = generate_dummy_pptx(text_input, guidance)
        
        return StreamingResponse(
            pptx_io,
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            headers={"Content-Disposition": "attachment; filename=generated_presentation.pptx"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")
