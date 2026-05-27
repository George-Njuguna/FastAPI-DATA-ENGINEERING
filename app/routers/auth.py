from fastapi import APIRouter, Depends, status
from .. import schemas, db 
from ..services import auth
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/auth",
    tags=["Authentification"] # Groups endpoints together neatly in Swagger UI
)

@router.post("/login", response_model = schemas.TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db.get_db)):

    credentials = schemas.LoginRequest(
        email=form_data.username,
        password=form_data.password
    )

    return auth.AuthService.auth_user_and_create_token(db, credentials)