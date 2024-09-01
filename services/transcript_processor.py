from models.models import Transcript

def process_transcript_data(transcript: Transcript) -> dict:
    # TODO: Implement transcript processing logic
    return {
        "id": transcript.id,
        "title": transcript.title,
        "duration": transcript.duration,
        "summary": transcript.summary,
        "action_items": transcript.action_items,
        "questions": transcript.questions,
    }
