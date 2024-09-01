from fastapi import HTTPException, Request
from core.config import settings
import hmac
import hashlib

async def verify_fireflies_signature(request: Request, x_fireflies_signature: str):
    if not settings.FIREFLIES_WEBHOOK_SECRET:
        raise HTTPException(status_code=500, detail="Webhook secret not configured")

    body = await request.body()
    computed_signature = hmac.new(settings.FIREFLIES_WEBHOOK_SECRET.encode(), body, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(computed_signature, x_fireflies_signature):
        raise HTTPException(status_code=401, detail="Invalid signature")
