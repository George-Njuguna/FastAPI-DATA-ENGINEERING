from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_user_email(token : str = Depends(oauth2_scheme)) -> str :

    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers = {"WWW-Authenticate": "Bearer"},
    )

    try:

        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        return email
    
    except JWTError:
        raise credentials_exception
    
class RoleChecker:

    def __init__(self , allowed_roles : list[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, token : str = Depends(oauth2_scheme)) -> dict:

        exception = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation rejected: Insufficient pipeline permissions."
        )
        
        try:

            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_role : str  = payload.get("role")

            if user_role is not self.allowed_roles:
                raise exception 
            
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token context")
        
