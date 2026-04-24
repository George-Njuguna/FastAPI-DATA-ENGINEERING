from fastapi import FastAPI ,HTTPException, Depends
import logging
from pydantic import BaseModel, Field, EmailStr, field_validator , ConfigDict
from typing import List, Annotated
from pydantic.functional_validators import AfterValidator
from uuid import uuid4, UUID
from sqlalchemy.orm import Session
from datetime import datetime
from .db import get_db
import .

# Simulating Database
Users_db = []
Products_db = []

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.get("/")
def root():
    return {
        "message": "e-commerse  API is running" 
    }

 

#------------------------
# PRODUCT ENDPOINTS
#------------------------

@app.post("/products/", response_model = ProductOut)
def PostProduct(product_info : ProductUpdate, storage = Depends(get_db)):
    logger.info(f"New product Added")
    new_product =  ProductOut(
        name = product_info.name,
        price = product_info.price,
        description = product_info.description
    )
    Products_db.append(new_product)
    return new_product

@app.get("/products/", response_model = ProductOut)
def get_product():
    return Products_db

#---------------------------
# USER ENDPOINTS
#---------------------------

@app.post("/create-user/", response_model = UserOut)
def CreateNewUserAccount(user_info : UserCreate):
    logger.info(f"New Account Created")
    return UserOut(
        first_name=user_info.first_name,
        second_name=user_info.second_name,
        email=user_info.email
    )

@app.get("/user/", response_model = UserOut)
def GetUserInfo():
    return Users_db
