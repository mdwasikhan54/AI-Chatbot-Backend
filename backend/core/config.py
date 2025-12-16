import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    """Project configuration settings."""
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "AI Chatbot")
    PROJECT_VERSION: str = os.getenv("PROJECT_VERSION", "1.0.0")

    # Database connection string (PostgreSQL/NeonDB)
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    # Security settings for JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # OpenAI API Key (Optional for mock service)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")

settings = Settings()