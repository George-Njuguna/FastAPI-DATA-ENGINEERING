import bcrypt
from datetime import datetime, timezone, timedelta
from jose import jwt
from .config import settings



class SecurityHandler:
    @staticmethod

    def hash_password( password : str ) -> str:
        hashed = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        )
        return hashed.decode("utf-8")
    
    @staticmethod
    def  verify_password( str_password : str , hashed_password : str ) -> bool:
        return bcrypt.checkpw(
            str_password.encode("utf-8"),
            hashed_password.encode("utf-8")
    )
    

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

