from fastapi import Depends
from sqlalchemy.orm import Session

from ..db import get_db
from ..services.pipelines import FileIngestionService

# creating an independent file service 
def get_independent_file_service():
    return FileIngestionService