from ..services.users import UserService
from ..services.auth import RoleChecker
from .. import schemas, db 
from ..dependancies.users import get_user_service
from fastapi import FastAPI ,HTTPException, Depends, APIRouter
from typing import List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/users",
    tags=["Users Operations "] 
)


@router.post("/create-user/", response_model = schemas.UserOut)
def CreateNewUserAccount(
    user_info : schemas.UserCreate, 
    service : UserService = Depends( get_user_service ) , 
    current_user = Depends( RoleChecker(["engineer","admin"]) )
    ):

    logger.info(f"New Account Created")

    return service.create_user(data = user_info)


@router.get("/user/{id}", response_model = schemas.UserOut)
def GetUserInfo( 
    id : int,
    service : UserService = Depends( get_user_service ) , 
    current_user = Depends(RoleChecker(["engineer","admin"]))
    ):

    logger.info(f"Getting info of User {id}")
    return( service.get_user_by_id( id = id ) )

@router.get("/total-user/", response_model = schemas.UserStats)
def GetNumberofUsers( 
    service : UserService = Depends( get_user_service ) , 
    current_user = Depends(RoleChecker(["analyst","admin"]) ) ):

    logger.info(f"Getting Total Users")
    return( service.get_total_users() )
