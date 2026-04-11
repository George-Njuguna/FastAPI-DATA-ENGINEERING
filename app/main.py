from fastapi import FastAPI
import logging
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import List, Annotated
from pydantic.functional_validators import AfterValidator
import uuid
from sqlmodel import SQLModel, Field


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
    v.strip().title()

 # clean price normalization
def clean_price( v, int ) -> int:
    v.strip(',')


CleanPassword = Annotated[
    str,
    Field(
        regex = r"(?=.*\d)(?=.*\w)(?=.*[^A-Za-z0-9]).{8,12}$"
    )
]
CleanName = Annotated[str, AfterValidator(clean_string)]
CleanPrice = Annotated[int, AfterValidator(clean_price)]

 # creating a customer model
class UserCreate(BaseModel): # This is internal 
    first_name : CleanName
    second_name : CleanName
    password : CleanPassword

    email : EmailStr
    @field_validator("email")
    @classmethod
    def email_normalization(cls, v) -> str:
        return v.strip().lower()


    
class UserOut(BaseModel):
    user_id :int
    first_name : CleanName
    second_name : CleanName
    email : EmailStr
    

 # creating a product model
class Product_Input(BaseModel):
    name : CleanName 
    price : CleanPrice
    description : str | None = None 

@app.get("/user/{user_id}", response_model = UserOut)
def GetUserInfo( user_id : int ):
    return{
        "user_id" : user_id,
        "first_name" : "George",
        "second_name" : "Njuguna",
        "Password" : "Xotourlif3!",
        "email" : "example@email.com"
    }

