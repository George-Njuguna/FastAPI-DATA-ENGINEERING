from pydantic import BaseModel, Field, EmailStr, field_validator , ConfigDict
from typing import List, Annotated
from pydantic.functional_validators import AfterValidator
from datetime import datetime
from uuid import uuid4, UUID

 # clean name normalization 
def clean_string( v : str ) -> str:
    return v.strip().title()



CleanName = Annotated[str, AfterValidator(clean_string)]

#------------------------------
# CALCULATION MODELS 
#------------------------------
class ProductStats(BaseModel):
    total_count : int
    category : str | None = "all"
    generated_at : datetime

class UserStats(BaseModel):
    total_count : int
    category : str | None = "all"
    generated_at : datetime



#-------------------------------
# USER MODELS
#-------------------------------
class UserBase(BaseModel): # This is internal
    name : CleanName 
    


class UserCreate(UserBase):
    model_config = ConfigDict(extra='forbid') # This forbids any other data from being loaded 
    password : str
    email : EmailStr
   
    
class UserOut(UserBase):
    id: int
    created_at: datetime
    email : EmailStr

    class Config:
        from_attributes = True
    
#-------------------------------
# PRODUCT MODELS
#-------------------------------

class ProductBase(BaseModel):
    name : CleanName 
    price : int = Field( gt = 0 )
    product_details : str | None = None

class ProductCreate(ProductBase):
    pass


class ProductOut(ProductCreate):
    id : int
    created_at : datetime

    class Config:
        from_attributes = True