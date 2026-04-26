from . import models , schemas
from sqlalchemy.orm import Session
from sqlalchemy import select

def create_user(db: Session, user: schemas.UserCreate):
    # 1. Map Schema -> Model
    db_user = models.User(
        user_name = user.user_name,
        user_email = user.user_email,
        password = user.password
    )
    # 2. Stage and Commit
    db.add(db_user)
    db.flush()

    return db_user

def getUserbyId(db : Session, user_id : int):

    stmt = select( models.User ).where(models.User.user_id == user_id )

    result = db.execute(stmt)


    return result.scalar_one_or_none()

def getProductbyId(db : Session, product_id : int):
    stmt = select( models.Product ).where(models.Product.product_id == product_id)

    result = db.execute(stmt)

    return result.scalar_one_or_none() 


def create_product( db : Session, product : schemas.ProductBase):

    db_product = models.Product(
        product_name = product.product_name,
        price = product.price,
        product_details = product.product_details
    )

    db.add(db_product)
    db.flush()
    return db_product