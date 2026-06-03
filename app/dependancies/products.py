from fastapi import Depends
from sqlalchemy.orm import Session

from ..db import get_db
from ..services.products import ProductService

def get_product_service(
        db : Session = Depends( get_db )
):
    return ProductService( db )