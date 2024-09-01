from pydantic import BaseModel
from typing import List

class Speaker(BaseModel):
    name: str
    email: str

class Sentence(BaseModel):
    start_time: float
    end_time: float
    text: str
    speaker: str

class Transcript(BaseModel):
    id: str
    title: str
    room_name: str
    start_time: str
    end_time: str
    duration: int
    transcript: List[Sentence]
    speakers: List[Speaker]
    notes: List[str] = []
    topics: List[str] = []
    summary: str = ""
    action_items: List[str] = []
    questions: List[str] = []

class ProcessedData(BaseModel):
    summary: str
