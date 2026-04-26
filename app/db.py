from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from .config import settings
from dotenv import load_dotenv
from pathlib import Path
import os



engine = create_engine(str(settings.DB_URL))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()

    try:
        yield db 
        db.commit()  

    except:
        db.rollback() 
        raise
    
    finally:
        db.close()


def main():
    print("created postgres session")

if __name__ == "__main__":
    main()
