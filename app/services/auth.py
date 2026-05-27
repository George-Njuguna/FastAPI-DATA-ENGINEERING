from .. import securities, crud, schemas 
from fastapi import HTTPException , status
from sqlalchemy.orm import Session

# ----------------------
# AUTHENTICATION
# ----------------------
class AuthService:
    @staticmethod

    def auth_user_and_create_token(storage: Session, data: schemas.LoginRequest) -> schemas.TokenResponse:

        user = crud.get_user_by_email(storage, data.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid Email "
            )
        
        # check password 
        valid_password = securities.SecurityHandler.verify_password( data.password, user.password )
        if not valid_password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid Password"
            )

        # creating acess token 
        access_token = securities.SecurityHandler.create_access_token( data = {"sub": user.email, 
                                                                               "role": user.role} )

        return schemas.TokenResponse(
            access_token=access_token, 
            token_type="bearer"
        )
