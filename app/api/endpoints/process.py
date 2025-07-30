from fastapi import APIRouter, File, UploadFile
from typing import Dict

router = APIRouter()

@router.post("/process-flyer/")
async def process_flyer(file: UploadFile = File(...)) -> Dict[str, str]:
    """
    Accepts an image file and returns a confirmation.
    """
    return {
        "status": "success",
        "filename": file.filename or "",
        "content_type": file.content_type or "",
    }
