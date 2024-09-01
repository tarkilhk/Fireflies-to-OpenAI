# Meeting Transcript Processor

This project processes meeting transcripts using FastAPI and OpenAI.

## Setup
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables in `.env`
4. Run the server: `uvicorn main:app --reload`

## Docker
Build: `docker build -t meeting-transcript-processor .`
Run: `docker run -p 8000:8000 meeting-transcript-processor`