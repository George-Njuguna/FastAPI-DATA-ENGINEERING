from .. import securities, crud, schemas, config, db
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

    def get_current_user( token : str = Depends(oauth2_scheme), db: Session = Depends(db.get_db) ):

        credential_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unaurthorized"
        )

        try:

            payload = jwt.decode(token, config.settings.SECRET_KEY, algorithms=[config.settings.ALGORITHM])
            email : str = payload.get("sub")

            if email is None:
                raise credential_exception
                        
                    
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token context")
        
        user = crud.get_user_by_email(db, email)

        return user



    
    

class RoleChecker:
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user = Depends(AuthService.get_current_user)) -> dict:

        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Unauthorized"
            )
            
        return current_user





        
