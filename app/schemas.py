from pydantic import BaseModel, Field, EmailStr, field_validator , ConfigDict
from typing import List, Annotated
from pydantic.functional_validators import AfterValidator
from datetime import datetime
from uuid import uuid4, UUID

 # clean name normalization 
def clean_string( v : str ) -> str:
    return v.strip().title()



CleanName = Annotated[str, AfterValidator(clean_string)]

#----------------------------
# LOGIN
#----------------------------
class LoginRequest(BaseModel):
    email : EmailStr
    password : str

# -----------------------
# TOKEN
# -----------------------
class TokenResponse(BaseModel):
    access_token : str
    refresh_token : str
    token_type : str 

class RefreshToken(BaseModel):
    access_token : str
    token_type : str 

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

class BulkProductLoad(BaseModel):
    inserted : int
    status : str 


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
    sku : str 
    name : CleanName 
    price : int = Field( gt = 0 )
    details : str | None = None

class ProductCreate(ProductBase):
    pass


class ProductOut(ProductCreate):
    id : int
    sku : str
    created_at : datetime

    class Config:
        from_attributes = True