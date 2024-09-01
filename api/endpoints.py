from fastapi import APIRouter, Request, Header
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models.models import Transcript, ProcessedData
from services.transcript_processor import process_transcript_data
from services.openai_service import send_to_openai
from core.security import verify_fireflies_signature

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/process-transcript", response_model=ProcessedData)
async def process_transcript(
    request: Request, 
    transcript: Transcript, 
    x_fireflies_signature: str = Header(None)
):
    await verify_fireflies_signature(request, x_fireflies_signature)
    processed_data = process_transcript_data(transcript)
    openai_response = await send_to_openai(processed_data)
    return ProcessedData(summary=openai_response)

@router.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is operational"}