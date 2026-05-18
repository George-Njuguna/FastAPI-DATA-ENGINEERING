from passlib.context import CryptContext

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