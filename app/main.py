from fastapi import FastAPI ,HTTPException, Depends
import logging
from pydantic import BaseModel, Field, EmailStr, field_validator , ConfigDict
from typing import List, Annotated
from pydantic.functional_validators import AfterValidator
from uuid import uuid4, UUID
from sqlalchemy.orm import Session
from datetime import datetime
from . import schemas, db, crud, services

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

@app.get("/products/{product_id}", response_model = schemas.ProductOut)
def GetProductInfo( product_id : int, storage = Depends(db.get_db)):
    logger.info(f"Getting info of product {product_id}")
    return( crud.getProductbyId( db = storage , product_id = product_id ) )

@app.get("/total-products/")
def GetNumberofProducts( storage = Depends(db.get_db)):
    logger.info(f"Getting Total products")
    return( services.get_total_products( db = storage ) )
    

#---------------------------
# USER ENDPOINTS
#---------------------------

@app.post("/create-user/", response_model = schemas.UserOut)
def CreateNewUserAccount(user_info : schemas.UserCreate, storage = Depends(db.get_db)):

    logger.info(f"New Account Created")
    return crud.create_user( db = storage, user = user_info)


@app.get("/user/{user_id}", response_model = schemas.UserOut)
def GetUserInfo( user_id : int, storage = Depends(db.get_db)):
    logger.info(f"Getting info of User {user_id}")
    return( crud.getUserbyId( db = storage , user_id = user_id ) )

@app.get("/total-user/")
def GetNumberofUsers( storage = Depends(db.get_db)):
    logger.info(f"Getting Total Users")
    return( services.get_total_users( db = storage ) )


