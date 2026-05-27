from fastapi import FastAPI ,HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
import logging
from pydantic import BaseModel, Field, EmailStr, field_validator , ConfigDict
from typing import List, Annotated
from pydantic.functional_validators import AfterValidator
from uuid import uuid4, UUID
from sqlalchemy.orm import Session
from datetime import datetime
from . import schemas, db, services, auth


app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

allow_engineers = auth.RoleChecker(["admin","engineer"])
allow_analysts = auth.RoleChecker(["admin","analyst"])
allow_viewers = auth.RoleChecker(["admin","engineer","analyst","viewer"])



@app.get("/")
def root():
    return {
        "message": "e-commerse  API is running" 
    }

# ----------------------------
# AUTHENTIFICATION ENDPOINTS
# ----------------------------

@app.post("/login/", response_model = schemas.TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db.get_db)):

    credentials = schemas.LoginRequest(
        email=form_data.username,
        password=form_data.password
    )
    
    return services.AuthService.auth_user_and_create_token(db, credentials)
#------------------------
# PRODUCT ENDPOINTS
#------------------------

@app.post("/product/", response_model = schemas.ProductOut )
def PostProduct(product_info : schemas.ProductCreate, storage = Depends(db.get_db), token_context: dict = Depends(allow_engineers)):
    logger.info(f"New product Added")
    return services.ProductService.create_product( db = storage, data = product_info)

@app.get("/products/{id}", response_model = schemas.ProductOut)
def GetProductInfo( id : int, storage = Depends(db.get_db), token_context: dict = Depends(allow_viewers)):
    logger.info(f"Getting info of product {id}")
    return( services.ProductService.get_product_by_id( db = storage , id = id ) )

@app.get("/total-products/", response_model = schemas.ProductStats)
def GetNumberofProducts( storage = Depends(db.get_db), token_context: dict = Depends(allow_viewers)):
    logger.info(f"Getting Total products")
    return( services.ProductService.get_total_products( db = storage ) )

@app.post("/products/", response_model = schemas.BulkProductLoad )
def BulkProductsLoad( products  : List[schemas.ProductCreate], storage = Depends(db.get_db), token_context: dict = Depends(allow_engineers)):
    logger.info(f"Loading Bulk Data")
    return( services.ProductService.create_bulk_products(db = storage, data = products))
    

#---------------------------
# USER ENDPOINTS
#---------------------------

@app.post("/create-user/", response_model = schemas.UserOut)
def CreateNewUserAccount(user_info : schemas.UserCreate, storage = Depends(db.get_db)):

    logger.info(f"New Account Created")
    return services.UserService.create_user( db = storage, data = user_info)


@app.get("/user/{id}", response_model = schemas.UserOut)
def GetUserInfo( id : int, storage = Depends(db.get_db), token_context: dict = Depends(allow_analysts)):
    logger.info(f"Getting info of User {id}")
    return( services.UserService.get_user_by_id( db = storage , id = id ) )

@app.get("/total-user/", response_model = schemas.UserStats)
def GetNumberofUsers( storage = Depends(db.get_db), token_context: dict = Depends(allow_analysts)):
    logger.info(f"Getting Total Users")
    return( services.UserService.get_total_users( db = storage ) )


