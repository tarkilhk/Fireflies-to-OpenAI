# main.py

from fastapi import FastAPI, HTTPException, Depends, Header, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx
import os
from dotenv import load_dotenv
from models.models import Transcript, ProcessedData
import hmac
import hashlib

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Meeting Transcript Processor",
    description="A service to process meeting transcripts and interact with OpenAI API",
    version="1.0.0",
)

# Fireflies webhook authentication
async def verify_fireflies_signature(request: Request, x_fireflies_signature: str = Header(None)):
    webhook_secret = os.getenv("FIREFLIES_WEBHOOK_SECRET")
    if not webhook_secret:
        raise HTTPException(status_code=500, detail="Webhook secret not configured")

    body = await request.body()
    computed_signature = hmac.new(webhook_secret.encode(), body, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(computed_signature, x_fireflies_signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

# Endpoints
@app.post("/process-transcript", response_model=ProcessedData)
async def process_transcript(request: Request, transcript: Transcript, x_fireflies_signature: str = Header(None)):
    """
    Process a meeting transcript from Fireflies.ai
    """
    await verify_fireflies_signature(request, x_fireflies_signature)
    processed_data = process_transcript_data(transcript)
    openai_response = await send_to_openai(processed_data)
    return ProcessedData(summary=openai_response)

# Processing functions
def process_transcript_data(transcript: Transcript) -> dict:
    # TODO: Implement transcript processing logic
    # For now, we'll just return a simplified version of the transcript
    return {
        "id": transcript.id,
        "title": transcript.title,
        "duration": transcript.duration,
        "summary": transcript.summary,
        "action_items": transcript.action_items,
        "questions": transcript.questions,
    }

async def send_to_openai(data: dict) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.openai.com/v1/engines/davinci-codex/completions",
            headers={
                "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
                "Content-Type": "application/json",
            },
            json={
                "prompt": str(data),
                "max_tokens": 100,
            },
        )
    response.raise_for_status()
    return response.json()["choices"][0]["text"]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

