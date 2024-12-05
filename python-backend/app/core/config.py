from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = ENVIRONMENT == "development"
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Botify API"
    HOST: str = "0.0.0.0"
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Security Settings
    EXTENSION_ID: str = os.getenv("EXTENSION_ID", "")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60 if ENVIRONMENT == "production" else 200
    
    # CORS Settings
    BACKEND_CORS_ORIGINS: List[str] = [
        "chrome-extension://*",
        "http://localhost:3000",
        "http://localhost:8000",
    ]
    
    # AI Model Settings
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # MongoDB Settings
    MONGODB_URI: Optional[str] = os.getenv("MONGODB_URI")
    MONGODB_DB_NAME: str = "botify"
    MONGODB_COLLECTION: str = "conversations"
    
    # Pinecone Settings
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY", "")
    PINECONE_ENVIRONMENT: str = os.getenv("PINECONE_ENVIRONMENT", "us-west-2")
    PINECONE_INDEX_NAME: str = os.getenv("PINECONE_INDEX_NAME", "botify-index")

    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "allow"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
