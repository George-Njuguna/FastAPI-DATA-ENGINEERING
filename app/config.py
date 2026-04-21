from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pathlib import Path
import os


env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv( env_path )

class Settings(BaseSettings):
    DB_URL: str = f"postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PW")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}"
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "DataIngestion"

    class Config:
        env_file = env_path


settings = Settings()