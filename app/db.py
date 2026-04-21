from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from .config import settings
from dotenv import load_dotenv
from pathlib import Path
import os



engine = create_engine(settings.DB_URL())

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def main():
    print("created postgres session")

if __name__ == "__main__":
    main()
