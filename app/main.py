from fastapi import FastAPI ,HTTPException, Depends
import logging
from pydantic import BaseModel, Field, EmailStr, field_validator , ConfigDict
from typing import List, Annotated
from pydantic.functional_validators import AfterValidator
from uuid import uuid4, UUID
from sqlalchemy.orm import Session
from datetime import datetime
from db import SessionLocal, engine

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

 # clean name normalization 
def clean_string( v : str ) -> str:
    return v.strip().title()



CleanName = Annotated[str, AfterValidator(clean_string)]

#-------------------------------
# DEPENDANCY INJECTION
#-------------------------------
def get_db():
    db = SessionLocal()

    try:
        yield db 
    finally:
        db.close()

#-------------------------------
# USER MODELS
#-------------------------------
class UserBase(BaseModel): # This is internal
    first_name : CleanName
    second_name : CleanName


class UserCreate(UserBase):
    model_config = ConfigDict(extra='forbid') # This forbids any other data from being loaded 
    password : str
    email : EmailStr
    @field_validator("email")
    @classmethod
    def email_normalization(cls, v) -> str:
        return v.strip().lower()
    
    
class UserOut(UserBase):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    email : EmailStr
    
#-------------------------------
# PRODUCT MODELS
#-------------------------------

class ProductBase(BaseModel):
    name : CleanName 
    price : int = Field( gt = 0 )
    description : str | None = None

class ProductUpdate(ProductBase):
    pass


class ProductOut(ProductBase):
    id : UUID = Field(default_factory=uuid4)
    created_at : datetime = Field(default_factory=datetime.utcnow)

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
