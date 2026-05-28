import bcrypt
from fastapi import HTTPException, status
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
    
    @staticmethod
    def create_access_token( data : dict, expiry_delta : timedelta | None = None ) -> str:

        to_encode = data.copy()

        if expiry_delta:
            expire = datetime.now ( timezone.utc ) + expiry_delta

        else:
            expire = datetime.now( timezone.utc ) + timedelta( minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES )

        to_encode.update(
            {"exp": int( expire.timestamp()),
             "type": "access"}
            )

        encoded_jwt = jwt.encode(
            to_encode, 
            settings.SECRET_KEY, 
            algorithm=settings.ALGORITHM
        )
        return encoded_jwt
    
    @staticmethod
    def create_refresh_token( data : dict ) -> str:

        to_encode = data.copy()
        expire = datetime.now( timezone.utc ) + timedelta( days = settings.REFRESH_TOKEN_EXPIRE )
        to_encode.update(
            {"exp": int( expire.timestamp() ),
             "type": "refresh"}
            )
        
        encoded_jwt = jwt.encode(
            to_encode, 
            settings.SECRET_KEY, 
            algorithm=settings.ALGORITHM
        )
        return encoded_jwt
    







