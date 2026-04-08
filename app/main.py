from fastapi import FastAPI
import logging
from pydantic import BaseModel, Field, EmailStr, field_validator


app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.get("/")
def root():
    return {
        "message": "e-commerse  API is running" 
    }

 # clean name normalization 

 # creating a customer model
class Customer(BaseModel):
    name : str 

    email : EmailStr
    @field_validator("email")
    @classmethod
    def email_normalization(cls, v) -> str:
        return v.strip().lower()


 # creating a product model
class Product(BaseModel):
    name : str 
    price : int = Field( gt = 0 )
    description : str | None = None 
