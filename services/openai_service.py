import httpx
from core.config import settings
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def retrieve_gpt_file(filename: str = "meeting_transcripts.json") -> str:
    files = client.files.list()
    for file in files.data:
        if file.filename == filename:
            return file.id
    raise FileNotFoundError(f"File '{filename}' not found in the OpenAI account")

def list_assistant_files(assistant_id: str):
    try:
        assistant = client.beta.assistants.retrieve(assistant_id)
        return assistant.file_ids
    except Exception as e:
        raise ValueError(f"Failed to list assistant files: {str(e)}")

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

def upload_to_gpt(json_data: str) -> bool:
    response = client.files.upload(file=json_data, purpose="fine-tune")
    return response.status_code == 200

def remove_gpt_file(file_id: str) -> None:
    client.files.delete(file_id)
