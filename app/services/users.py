from .. import schemas, crud
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException , status

class UserService:

    def __init__(self , db : Session):

        self.db = db 
        
    def create_user(self, data: schemas.UserCreate):

        existing_user = crud.get_user_by_email( self.db, data.email )

        if existing_user:
            raise HTTPException(
                status_code=409,
                detail="User already exists."
            )
        
        try:

            new_user = crud.add_user( db, data )
            
            self.db.flush() 
            self.db.commit()
            
            return new_user

        except Exception as e:

            self.db.rollback()
            raise HTTPException( status_code = 400, detail = " User Registration failed." ) 
        
    @staticmethod   
    def get_total_users(db: Session , category : str | None = None ) -> int :

        count = crud.get_total_users(db)

        return schemas.UserStats(
            total_count = count,
            category = category or "all",
            generated_at = datetime.now()
        )

    @staticmethod
    def get_user_by_id( db: Session, id: int ):

        user = crud.get_user_by_id( db, id )

        if not user:
            raise HTTPException(
                status_code=404, 
                detail=f"User with ID {id} does not exist in our records."
            )
            
        return user