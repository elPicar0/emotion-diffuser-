import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Model Configuration
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
    
    # Thresholds
    ESCALATION_THRESHOLD: float = float(os.getenv("ESCALATION_THRESHOLD", "0.7"))
    TOXICITY_THRESHOLD: float = float(os.getenv("TOXICITY_THRESHOLD", "0.6"))
    
    # Debug
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))


settings = Settings()
