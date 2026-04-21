from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pathlib import Path


env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv( env_path )

class Settings(BaseSettings):

    DB_USER: str
    DB_PW: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    def DB_URL(self) -> str:
        return (
            f"postgresql://{self.DB_USER}:"
            f"{self.DB_PW}@"
            f"{self.DB_HOST}:"
            f"{self.DB_PORT}/"
            f"{self.DB_NAME}"
        )

    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "DataIngestion"

    class Config:
        env_file = env_path


settings = Settings()