"""Configuration management for SmartAdvisor backend."""
import os
from typing import List
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings."""
    
    def __init__(self):
        # LLM Provider Configuration
        self.llm_provider: str = os.getenv("LLM_PROVIDER", "openai")
        self.openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
        self.openai_model: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        
        # Azure OpenAI Configuration
        self.azure_openai_endpoint: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
        self.azure_openai_api_key: str = os.getenv("AZURE_OPENAI_API_KEY", "")
        self.azure_openai_deployment_name: str = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "")
        self.azure_openai_api_version: str = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
        
        # OpenRouter Configuration
        self.openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")
        self.openrouter_model: str = os.getenv("OPENROUTER_MODEL", "openai/gpt-3.5-turbo")
        self.openrouter_base_url: str = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        
        # Server Configuration
        self.host: str = os.getenv("HOST", "0.0.0.0")
        self.port: int = int(os.getenv("PORT", "8000"))
        cors_origins_str = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173")
        self.cors_origins: List[str] = [origin.strip() for origin in cors_origins_str.split(",")]
        
        # Database Configuration
        # Heroku provides DATABASE_URL automatically, fallback to SQLite for local dev
        self.database_url: str = os.getenv("DATABASE_URL") or os.getenv("HEROKU_DATABASE_URL") or "sqlite:///./smartadvisor.db"
        
        # Logging Configuration
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")
        self.log_file: str = os.getenv("LOG_FILE", "logs/smartadvisor.log")


settings = Settings()

