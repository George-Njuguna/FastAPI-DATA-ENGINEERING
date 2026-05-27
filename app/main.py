from fastapi import FastAPI ,HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
import logging
from typing import List
from sqlalchemy.orm import Session
from . import schemas, db, services, auth
from .routers import auth, pipelines, products, users


app = FastAPI( title = "Data Engineering with Fast API" )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Connect the Department Routers to the Main Building
app.include_router(auth.router, prefix="/api/v1")
app.include_router(products.router, prefix="/api/v1")
#app.include_router(pipelines.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")

@app.get("/")
def health_check():
    return {"status": "healthy", "environment": "production"}


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


