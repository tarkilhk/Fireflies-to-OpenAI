import httpx
from core.config import settings

async def send_to_openai(data: dict) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.openai.com/v1/engines/davinci-codex/completions",
            headers={
                "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "prompt": str(data),
                "max_tokens": 100,
            },
        )
    response.raise_for_status()
    return response.json()["choices"][0]["text"]
