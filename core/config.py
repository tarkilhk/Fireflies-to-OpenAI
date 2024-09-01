from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Meeting Transcript Processor"
    PROJECT_DESCRIPTION: str = "A service to process meeting transcripts from Fireflies.ai and interact with OpenAI API"
    VERSION: str = "1.0.0"
    FIREFLIES_WEBHOOK_SECRET: str
    OPENAI_API_KEY: str
    api_key: str  # Add this line

    class Config:
        env_file = ".env"

settings = Settings()
