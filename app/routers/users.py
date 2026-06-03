from ..services import users, auth
from .. import schemas, db 
from fastapi import FastAPI ,HTTPException, Depends, APIRouter
from typing import List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/users",
    tags=["Users Operations "] # Groups endpoints together neatly in Swagger UI
)

@router.post("/create-user/", response_model = schemas.UserOut)
def CreateNewUserAccount(user_info : schemas.UserCreate, storage = Depends(db.get_db) , current_user = Depends(auth.RoleChecker(["engineer","admin"]))):

    logger.info(f"New Account Created")
    return users.UserService.create_user( db = storage, data = user_info)


@router.get("/user/{id}", response_model = schemas.UserOut)
def GetUserInfo( id : int, storage = Depends(db.get_db), current_user = Depends(auth.RoleChecker(["engineer","admin"]))):
    logger.info(f"Getting info of User {id}")
    return( users.UserService.get_user_by_id( db = storage , id = id ) )

@router.get("/total-user/", response_model = schemas.UserStats)
def GetNumberofUsers( storage = Depends(db.get_db), current_user = Depends(auth.RoleChecker(["analyst","admin"]) ) ):
    logger.info(f"Getting Total Users")
    return( users.UserService(storage).get_total_users())
