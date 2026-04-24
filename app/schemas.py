from pydantic import BaseModel, Field, EmailStr, field_validator , ConfigDict
from typing import List, Annotated
from pydantic.functional_validators import AfterValidator
from datetime import datetime
from uuid import uuid4, UUID

 # clean name normalization 
def clean_string( v : str ) -> str:
    return v.strip().title()



CleanName = Annotated[str, AfterValidator(clean_string)]



#-------------------------------
# USER MODELS
#-------------------------------
class UserBase(BaseModel): # This is internal
    name : CleanName = Field(gt =  0 , lt = 2)
    


class UserCreate(UserBase):
    model_config = ConfigDict(extra='forbid') # This forbids any other data from being loaded 
    password : str
    email : EmailStr
    @field_validator("email")
    @classmethod
    def email_normalization(cls, v) -> str:
        return v.strip().lower()
    
    
class UserOut(UserBase):
    id: UUID
    created_at: datetime
    email : EmailStr
    
#-------------------------------
# PRODUCT MODELS
#-------------------------------

class ProductBase(BaseModel):
    name : CleanName = Field( lt = 2 )
    price : int = Field( gt = 0 )
    description : str | None = None

class ProductUpdate(ProductBase):
    pass


class ProductOut(ProductBase):
    id : UUID 
    created_at : datetime