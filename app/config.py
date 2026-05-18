import os 
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):

    DB_URL : PostgresDsn
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "DataIngestion"

    SECRET_KEY : str = os.get_env("JWT_SECRET_KEY", "DEVELOPMENT_INSECURE_FALLBACK_KEY_MUST_CHANGE")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30    

    model_config = SettingsConfigDict(
        env_file = str(ENV_FILE),
        env_file_encoding = 'utf-8',
        case_sensitiv = True  
    )


settings = Settings()