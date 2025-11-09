from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path

class Settings(BaseSettings):
    # API Configuration
    APP_NAME: str = "Agentic Roadmap API"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Database
    DATABASE_URL: str = "sqlite:///./roadmap.db"
    
    # LLM Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = "gpt-4o-mini"  # Cost-effective for development
    OPENAI_MAX_TOKENS: int = 1000
    OPENAI_TEMPERATURE: float = 0.7
    
    # Alternative: Anthropic Claude
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    ANTHROPIC_MODEL: str = "claude-3-haiku-20240307"
    
    # Groq API
    GROQ_KEY: str = os.getenv("GROQ_KEY", "")
    GROQ_MODEL: str = "llama3-70b-8192"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    
    # Conversation Settings
    MAX_CONVERSATION_TURNS: int = 50
    SESSION_TIMEOUT_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create global settings instance
settings = Settings()