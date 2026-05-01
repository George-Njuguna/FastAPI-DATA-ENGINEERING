from . import crud, schemas
from sqlalchemy.orm import Session
from datetime import datetime

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
    

def get_total_users(db: Session , category : str | None = None ) -> int :

    try:

        count = crud.get_total_users(db)
        db.flush() 
        db.commit()
        db.refresh(count)

        return schemas.UserStats(
            total_count = count,
            category = category,
            generated_at = datetime.now()
        )
    
    except Exception as e:

        db.rollback()
        raise e
    

def get_total_products(db: Session , category : str | None = None ) -> int :

    try:

        count = crud.get_total_products(db)
        db.flush() 
        db.commit()
        db.refresh(count)

        return schemas.ProductStats(
            total_count = count,
            category = category,
            generated_at = datetime.now()
        )
    
    except Exception as e:

        db.rollback()
        raise e


def get_user_by_id( db: Session, id: int ):

    try: 

        user = crud.getUserbyId( db, id )
        db.flush() 
        db.commit()
        db.refresh(user)

        return user
    
    except Exception as e:

        db.rollback()
        raise e

def get_product_by_id( db: Session, id: int ):

    try: 

        product = crud.getProductbyId( db, id )
        db.flush() 
        db.commit()
        db.refresh(product)

        return product
    
    except Exception as e:

        db.rollback()
        raise e