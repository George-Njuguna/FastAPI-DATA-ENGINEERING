from fastapi import Depends
from sqlalchemy.orm import Session

from ..db import get_db
from ..services.users import UserService

def get_user_service(
        db : Session = Depends(get_db)
):
    return UserService(db)