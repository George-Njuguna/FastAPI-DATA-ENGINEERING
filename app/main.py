from fastapi import FastAPI
import logging
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import List, Annotated
from pydantic.functional_validators import AfterValidator
from uuid import uuid4, UUID
from datetime import datetime



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

 # clean price normalization
def clean_price( v, int ) -> int:
    return v.strip(',')



CleanName = Annotated[str, AfterValidator(clean_string)]
CleanPrice = Annotated[int, AfterValidator(clean_price)]

 # creating a customer model
class UserBase(BaseModel): # This is internal
    first_name : CleanName
    second_name : CleanName


class UserCreate(UserBase):
    password : str
    email : EmailStr
    @field_validator("email")
    @classmethod
    def email_normalization(cls, v) -> str:
        return v.strip().lower()
    
class UserOut(UserBase):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    

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

@app.post("/create-user/", response_model = UserOut)
def CreateNewUserAccount(user_info : UserCreate):
    logger.info(f"New Account Created")
    return UserOut(
        first_name=user_info.first_name,
        second_name=user_info.second_name,
        email=user_info.email
    )


