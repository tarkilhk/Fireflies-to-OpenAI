# main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.endpoints import router
from core.config import settings

def retrieve_gpt_file(filename: str = "meeting_transcripts.json") -> str:
    files = client.files.list()
    for file in files.data:
        if file.filename == filename:
            return file.id
    raise FileNotFoundError(f"File '{filename}' not found in the OpenAI account")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
)

app.include_router(router)

import httpx
from core.config import settings
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
retrieve_gpt_file("meeting_transcripts.json")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

