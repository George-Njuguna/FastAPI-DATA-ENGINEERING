from pydantic import BaseSettings, PostgresDsn
from dotenv import load_dotenv
from pathlib import Path


env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv( env_path )

class Settings(BaseSettings):

    DB_URL = PostgresDsn
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "DataIngestion"

    class Config:
        env_file = env_path


settings = Settings()