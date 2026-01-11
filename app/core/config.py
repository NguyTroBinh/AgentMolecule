# app/core/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GROQ_API_KEY: str
    REDIS_URL: str = "redis://localhost:6379/0"
    DATABASE_URL: str = "sqlite:///./database.db"

    # Model configuration   
    PLANNER_MODEL: str = "llama-3.3-70b-versatile"      # Smart
    GENERATOR_MODEL: str = "llama-3.1-8b-instant"       # Fast
    RANKER_MODEL: str = "llama-3.3-70b-versatile"       # Smart

    class Config:
        env_file = ".env"

settings = Settings()