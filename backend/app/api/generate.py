from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse
from typing import Optional
from app.services.dummy_generator import generate_dummy_pptx

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
        pptx_io = generate_dummy_pptx(text_input, guidance)
        
        return StreamingResponse(
            pptx_io,
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            headers={"Content-Disposition": "attachment; filename=generated_presentation.pptx"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")
