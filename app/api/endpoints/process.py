from fastapi import APIRouter, File, UploadFile, HTTPException
from typing import Dict
import base64
import aiohttp
from app.core.config import settings

router = APIRouter()


def encode_image_to_base64(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode("utf-8")


async def extract_and_structure_from_image(data_url: str) -> Dict:
    print("Starting single-call extraction and structuring...")
    qwen_url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.openrouter_api_key}",
        "Content-Type": "application/json",
    }
    
    combined_payload = {
        "model": "qwen/qwen2.5-vl-72b-instruct:free",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """
                        Look at the attached event flyer image and convert its content directly into a structured JSON object.
                        Ensure the JSON object strictly adheres to the provided schema.
                        """
                    },
                    {"type": "image_url", "image_url": {"url": data_url}},
                ],
            }
        ],
        "response_format": { # <-- Your awesome schema goes here
            "type": "json_schema",
            "json_schema": {
                "name": "event_flyer",
                "strict": True,
                # ... (the rest of your schema is perfect)
                "schema": {
                    "type": "object",
                    "properties": {
                        "event_name": {"type": "string"},
                        "date": {"type": "string"},
                        "time": {"type": "string"},
                        "location": {"type": "string"},
                        "description": {"type": "string"},
                        "ticket_info": {"type": "string"},
                    },
                    "required": ["event_name", "date", "time", "location"],
                    "additionalProperties": False,
                },
            },
        },
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(qwen_url, headers=headers, json=combined_payload) as resp:
            result = await resp.json()

    print("Single-call processing complete.")
    if "choices" not in result or not result["choices"]:
        raise HTTPException(status_code=400, detail="AI model did not return a valid choice.")

    # The content is already the structured JSON you need
    return result["choices"][0]["message"]["content"]

async def perform_ocr(file: UploadFile) -> Dict:
    print("Reading and encoding image...")
    image_bytes = await file.read()
    base64_image = encode_image_to_base64(image_bytes)
    data_url = f"data:{file.content_type};base64,{base64_image}"

    structured_json = await extract_and_structure_from_image(data_url)
    print("OCR and conversion finished.")
    return structured_json


@router.post("/process-flyer/")
async def process_flyer(file: UploadFile = File(...)):
    """
    Accepts an image file and returns OCR result.
    Only supports webp, png, jpeg images.
    """
    supported_types = ["image/webp", "image/png", "image/jpeg"]
    if file.content_type not in supported_types:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file.content_type}. Supported types are: {', '.join(supported_types).replace('image/', '')}.",
        )

    print("Starting process_flyer endpoint...")
    info = await perform_ocr(file)
    print("process_flyer endpoint finished.")

    return {
        "status": "success",
        "filename": file.filename,
        "content_type": file.content_type,
        "info": info,
    }
