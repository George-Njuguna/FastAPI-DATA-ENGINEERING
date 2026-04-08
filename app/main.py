from fastapi import FastAPI
import logging
from pydantic import BaseModel, Field , EmailStr, field_validator, AfterValidator
from datetime import datetime, timezone
from uuid import uuid4
from typing import List, Annotated

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.get("/")
def root():
    return {
        "message": "Data Engineering API is running" 
    }

