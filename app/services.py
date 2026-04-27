from . import models , schemas
from sqlalchemy.orm import Session
from sqlalchemy import select,func

def get_total_users( db : Session ):

    stmt = select(func.count(models.User.user_id))

    result = db.scalar(stmt)


    return result



def get_total_products( db : Session ):

    stmt = select(func.count(models.Product.product_id))

    result = db.scalar(stmt)

    return result