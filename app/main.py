from fastapi import FastAPI ,HTTPException, Depends
import logging
from pydantic import BaseModel, Field, EmailStr, field_validator , ConfigDict
from typing import List, Annotated
from pydantic.functional_validators import AfterValidator
from uuid import uuid4, UUID
from sqlalchemy.orm import Session
from datetime import datetime
from . import schemas, db, crud 

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

@app.post("/products/", response_model = schemas.ProductOut)
def PostProduct(product_info : schemas.ProductUpdate, storage = Depends(db.get_db)):
    logger.info(f"New product Added")
    return crud.create_product( db = storage, product = product_info)

@app.get("/products/", response_model = schemas.ProductOut)
def get_product():
    return Products_db

#---------------------------
# USER ENDPOINTS
#---------------------------

@app.post("/create-user/", response_model = schemas.UserOut)
def CreateNewUserAccount(user_info : schemas.UserCreate, storage = Depends(db.get_db)):

    logger.info(f"New Account Created")
    return crud.create_user( db = storage, user = user_info)


@app.get("/user/", response_model = schemas.UserOut)
def GetUserInfo():
    return Users_db
