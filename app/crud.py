from . import models , schemas, securities
from sqlalchemy.orm import Session
from sqlalchemy import select,func 
from sqlalchemy.dialects.postgresql import insert

# ----------------------
# USER
#------------------------
def add_user(db: Session, user: schemas.UserCreate):
    # 1. Map Schema -> Model
    db_user = models.User(
        name = user.name,
        email = user.email,
        password = securities.SecurityHandler.hash_password(user.password)
    )
    # 2. Stage and Commit
    db.add(db_user)

    return db_user

def get_user_by_email(db: Session, email: str ):

    stmt = select( models.User ).where( models.User.email == email )
    result = db.execute(stmt)

    return result.scalar_one_or_none()

def get_user_by_id(db : Session, id : int):

    stmt = select( models.User ).where(models.User.id == id )
    result = db.execute(stmt)

    return result.scalar_one_or_none()

# -----------------------
# PRODUCTS
# -----------------------

def get_product_by_id(db : Session, id : int):

    stmt = select( models.Product ).where(models.Product.id == id)
    result = db.execute(stmt)

    return result.scalar_one_or_none() 


def add_product( db : Session, product : schemas.ProductBase):  # This is only used for one product at a time

    stmt = insert(models.Product).values(
        sku = product.sku,
        name = product.name,
        price = product.price,
        details = product.details
    )

    upsert_stmt = stmt.on_conflict_do_update(

        index_elements=["sku"], # checks if product sku exists if it exists it updates 

        set_={
            "name": product.name,
            "price": product.price,
            "details": product.details
        }

    ).returning(models.Product)

    result = db.execute(upsert_stmt)

    return result.scalar_one()

def add_product_bulk( db : Session, products : list[schemas.ProductBase]):

    deduped_data = {p.sku: p.model_dump() for p in products}

    stmt = insert(models.Product)

    upsert_stmt = stmt.on_conflict_do_update(

        index_elements = ["sku"],
        set_ = {
            "name" : stmt.excluded.name,
            "price" : stmt.excluded.price,
            "details" : stmt.excluded.details
        }
    )

    return db.execute(
        upsert_stmt, 
        list(deduped_data.values())
        )


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


def bulk_file_insert( db : Session):
    
    