from .. import securities, crud, schemas, config
from fastapi import HTTPException , status, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

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
                detail="Invalid Credentials "
            )
        
        # check password 
        valid_password = securities.SecurityHandler.verify_password( data.password, user.password )
        if not valid_password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid Credentials"
            )

        # creating acess token 
        access_token = securities.SecurityHandler.create_access_token( data = {"sub": user.email, 
                                                                               "role": user.role} )
        refresh_token = securities.SecurityHandler.create_refresh_token( data = {"sub": user.email, 
                                                                               "role": user.role} )

        return schemas.TokenResponse(
            access_token = access_token, 
            refresh_token = refresh_token,
            token_type = "bearer"
        )
    
    @staticmethod
    def refresh_token( refresh_token : str ) -> schemas.RefreshToken :

        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid or expired refresh token"
        )

        try:

            payload = jwt.decode(refresh_token, config.settings.SECRET_KEY, algorithms=[config.settings.ALGORITHM])
            

            if payload.get("type") != "refresh":
                raise exception
                
            email = payload.get("sub")

            if email is None:
                raise exception
                
            new_access_token = securities.SecurityHandler.create_access_token(data={"sub": email,
                                                                        "role": payload.get("role")})
            
            return schemas.RefreshToken(
                access_token = new_access_token, 
                token_type = "bearer"
            )           
            
        except JWTError:
            raise exception


    
    

class RoleChecker:

    def __init__(self , allowed_roles : list[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, token : str = Depends(oauth2_scheme)) -> dict:

        forbided_exception = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation rejected: Insufficient pipeline permissions."
        )

        credential_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unorthorized"
        )


        try:

            payload = jwt.decode(token, config.settings.SECRET_KEY, algorithms=[config.settings.ALGORITHM])
            user_role : str  = payload.get("role")
            
            if user_role not in self.allowed_roles:
                raise forbided_exception 
            
            
            return payload
            
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token context")
