from fastapi import FastAPI
import logging
from pydantic import BaseModel


app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.get("/")
def root():
    return {
        "message": "e-commerse  API is running" 
    }

 # creating a customer model
class Customer(BaseModel):
    name : str 
    email : str 


 # creating a product model
class Product(BaseModel):
    name : str 
    price : int
    description : str | None = None 
