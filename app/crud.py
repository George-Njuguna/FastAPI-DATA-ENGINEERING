from . import models , schemas
from sqlalchemy.orm import Session
from sqlalchemy import select,func 

# ----------------------
# USER
#------------------------
def add_user(db: Session, user: schemas.UserCreate):
    # 1. Map Schema -> Model
    db_user = models.User(
        name = user.name,
        email = user.email,
        password = user.password
    )
    # 2. Stage and Commit
    db.add(db_user)

    return db_user

def getUserbyEmail(db: Session, email: str ):

    stmt = select( models.User ).where( models.User.email == email )
    result = db.execute(stmt)

    return result.scalar_one_or_none()

def getUserbyId(db : Session, id : int):

    stmt = select( models.User ).where(models.User.user_id == id )
    result = db.execute(stmt)

    return result.scalar_one_or_none()

# -------------------------
# PRODUCTS
# -------------------------

def getProductbyId(db : Session, id : int):

    stmt = select( models.Product ).where(models.Product.id == id)
    result = db.execute(stmt)

    return result.scalar_one_or_none() 


def add_product( db : Session, product : schemas.ProductBase):

    db_product = models.Product(
        name = product.name,
        price = product.price,
        product_details = product.product_details
    )

    db.add(db_product)

    return db_product


def get_total_users( db : Session, category : str | None = None ):
    # add an if statement later when adding category 
    stmt = select(func.count(models.User.id))
    result = db.scalar(stmt)

    return result or 0



def get_total_products( db : Session, category : str | None = None ):
    # add an if statement later when adding category
    stmt = select(func.count(models.Product.id))
    result = db.scalar(stmt)

    return result or 0