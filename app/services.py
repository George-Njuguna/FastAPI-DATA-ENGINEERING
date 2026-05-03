from . import crud, schemas
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException

def create_user(db: Session, data: schemas.UserCreate):

    existing_user = crud.getUserbyEmail( db, data.email )

    if existing_user:
        print(f"User {data.email} already exists.")
    
    try:

        new_user = crud.add_user(db, data)
        
        db.flush() 
        db.commit()
        db.refresh(new_user)
        
        return new_user

    except Exception as e:

        db.rollback()
        raise HTTPException(status_code=400, detail=" User Registration failed.")
    

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

    count = crud.get_total_users(db)

    return schemas.UserStats(
        total_count = count,
        category = category or "all",
        generated_at = datetime.now()
    )


    

def get_total_products(db: Session , category : str | None = None ) -> int :

    count = crud.get_total_products(db)

    return schemas.ProductStats(
        total_count = count,
        category = category or "all",
        generated_at = datetime.now()
    )



def get_user_by_id( db: Session, id: int ):

    user = crud.getUserbyId( db, id )

    if not user:
        raise HTTPException(
            status_code=404, 
            detail=f"User with ID {id} does not exist in our records."
        )
        
    return user


def get_product_by_id( db: Session, id: int ):

    product = crud.getProductbyId( db, id )

    if not product:
        raise HTTPException(
            status_code=404, 
            detail=f"Product with ID {id} Not Found."
        )

    return product
