from . import crud, schemas
from sqlalchemy.orm import Session

def create_user(db: Session, data: schemas.UserCreate):
    try:

        new_user = crud.add_user(db, data)
        
        db.flush() 
        db.commit()
        db.refresh(new_user)
        
        return new_user

    except Exception as e:

        db.rollback()
        raise e
    

def create_product(db: Session, data: schemas.ProductCreate):
    try:

        new_user = crud.add_product(db, data)
        
        db.flush() 
        db.commit()
        db.refresh(new_user)
        
        return new_user

    except Exception as e:

        db.rollback()
        raise e