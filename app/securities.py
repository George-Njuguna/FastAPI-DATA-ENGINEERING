from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
from jose import jwt
from .config import settings

pwd_context = CryptContext(
    schemes=["bcrypt"], # this is the hashing 
    deprecated="auto"
)

class SecurityHandler:
    @staticmethod

    def hash_password( password : str ) -> str:
        return pwd_context.hash(password)
    
    @staticmethod
    def  verify_password( str_password : str , hashed_password : str ) -> bool:
        return pwd_context.verify( str_password , hashed_password )
    

def create_access_token( data : dict, expiry_delta : timedelta | None = None ) -> str:

    if expiry_delta:
        expire = datetime.now ( timezone.utc ) + expiry_delta

    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    data.update({"exp": int(expire.timestamp())})

    encoded_jwt = jwt.encode(
        data, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt