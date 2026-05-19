from . import crud, schemas, auth, securities 
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException , status


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
                detail="Invalid Email "
            )
        
        # check password 
        valid_password = securities.SecurityHandler.verify_password( data.password, user.password )
        if not valid_password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid Password"
            )
        
        # creating acess token 
        access_token = securities.SecurityHandler.create_access_token( data = {"sub": user.email} )

        return schemas.TokenResponse(
            access_token=access_token, 
            token_type="bearer"
        )

# -----------------------
# USER
# -----------------------
def create_user(db: Session, data: schemas.UserCreate):

    existing_user = crud.get_user_by_email( db, data.email )

    if existing_user:
        print(f"User {data.email} already exists.")
    
    try:

        new_user = crud.add_user( db, data )
        
        db.flush() 
        db.commit()
        
        return new_user

    except Exception as e:

        db.rollback()
        raise HTTPException( status_code = 400, detail = " User Registration failed." ) 
    

    
def get_total_users(db: Session , category : str | None = None ) -> int :

    count = crud.get_total_users(db)

    return schemas.UserStats(
        total_count = count,
        category = category or "all",
        generated_at = datetime.now()
    )


def get_user_by_id( db: Session, id: int ):

    user = crud.get_user_by_id( db, id )

    if not user:
        raise HTTPException(
            status_code=404, 
            detail=f"User with ID {id} does not exist in our records."
        )
        
    return user
    

# ---------------------
# PRODUCTS
# ---------------------
def create_product( db: Session, data: schemas.ProductCreate ):
    try:

        new_product = crud.add_product( db, data )
        
        db.flush() 
        db.commit()
        
        return new_product

    except Exception as e:

        db.rollback()
        raise e
    
def create_bulk_products( db : Session, data : list[schemas.ProductCreate] ):
    try:

        crud.add_product_bulk( db, data)

        db.commit()

        return {
            "inserted": len(data),
            "status": "success"
        }
    
    except Exception as e:

        db.rollback()
        raise e   

def get_total_products(db: Session , category : str | None = None ) -> int :

    count = crud.get_total_products(db)

    return schemas.ProductStats(
        total_count = count,
        category = category or "all",
        generated_at = datetime.now()
    )


def get_product_by_id( db: Session, id: int ):

    product = crud.get_product_by_id( db, id )

    if not product:
        raise HTTPException(
            status_code=404, 
            detail=f"Product with ID {id} Not Found."
        )

    return product
