from models.models import Transcript
import json
from typing import Dict
from services.openai_service import retrieve_gpt_file, upload_to_gpt, remove_gpt_file
from services.file_service import load_json_file
from services.transcript_formatter import format_transcript

def process_transcript_data(transcript: Transcript) -> dict:

    def process_transcript_data(transcript: Transcript) -> dict:
        gpt_file = retrieve_gpt_file()
        json_data = load_json_file(gpt_file)
        formatted_transcript = format_transcript(transcript)
        updated_json = append_transcript_to_json(json_data, formatted_transcript)
        
        if upload_new_file(updated_json):
            remove_previous_file(gpt_file)
        
        return formatted_transcript

    def append_transcript_to_json(json_data: Dict, formatted_transcript: Dict) -> Dict:
        json_data['transcripts'].append(formatted_transcript)
        return json_data

    def upload_new_file(updated_json: Dict) -> bool:
        return upload_to_gpt(json.dumps(updated_json))

    def remove_previous_file(file_id: str) -> None:
        remove_gpt_file(file_id)
    return {
        "id": transcript.id,
        "title": transcript.title,
        "duration": transcript.duration,
        "summary": transcript.summary,
        "action_items": transcript.action_items,
        "questions": transcript.questions,
    }
