from ..services import products, auth
from .. import schemas, db 
from fastapi import FastAPI ,HTTPException, Depends, APIRouter
from typing import List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/products",
    tags=["Products Catalog Operations "] # Groups endpoints together neatly in Swagger UI
)

allow_engineers = auth.RoleChecker(["engineer"])
allow_viewers = auth.RoleChecker(["viewer","engineer","admin"])
allow_admin = auth.RoleChecker(['admin'])

@router.post("/product/", response_model = schemas.ProductOut )
def PostProduct(product_info : schemas.ProductCreate, storage = Depends(db.get_db), token_context: dict = Depends(allow_engineers)):
    logger.info(f"New product Added")
    return products.ProductService.create_product( db = storage, data = product_info)

@router.get("/products/{id}", response_model = schemas.ProductOut)
def GetProductInfo( id : int, storage = Depends(db.get_db), token_context: dict = Depends(allow_viewers)):
    logger.info(f"Getting info of product {id}")
    return( products.ProductService.get_product_by_id( db = storage , id = id ) )

@router.get("/total-products/", response_model = schemas.ProductStats)
def GetNumberofProducts( storage = Depends(db.get_db), token_context: dict = Depends(allow_viewers)):
    logger.info(f"Getting Total products")
    return( products.ProductService.get_total_products( db = storage ) )

@router.post("/products/", response_model = schemas.BulkProductLoad )
def BulkProductsLoad( products  : List[schemas.ProductCreate], storage = Depends(db.get_db), token_context: dict = Depends(allow_engineers)):
    logger.info(f"Loading Bulk Data")
    return( products.ProductService.create_bulk_products(db = storage, data = products))
    