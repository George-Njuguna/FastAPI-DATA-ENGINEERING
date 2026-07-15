from ..services.auth import RoleChecker
from ..services.products import ProductService
from ..dependancies.products import get_product_service
from .. import schemas, db 
from fastapi import FastAPI ,HTTPException, Depends, APIRouter, Query
from typing import List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/products",
    tags=["Products Catalog Operations "]
)

allow_engineers = ["engineer","admin"]
allow_viewers = ["viewer","engineer","admin"]
allow_admin = ['admin']
allow_analysts = ["analyst", "admin" ]

@router.post("/product/", response_model = schemas.ProductOut )
def PostProduct(
    product_info : schemas.ProductCreate, 
    service : ProductService = Depends( get_product_service ), 
    current_user = Depends(RoleChecker( allow_engineers) )
):

    logger.info(f"New product Added")
    return service.create_product( data = product_info )

@router.get("/products/{id}", response_model = schemas.ProductOut)
def GetProductInfo( 
    id : int, 
    service : ProductService = Depends( get_product_service ), 
    current_user = Depends(RoleChecker( allow_viewers ))
):
    logger.info(f"Getting info of product {id}")
    return( service.get_product_by_id( id = id ) )

@router.get("/total-products/", response_model = schemas.ProductStats)
def GetNumberofProducts( 
    service : ProductService = Depends( get_product_service ), 
    current_user = Depends(RoleChecker( allow_viewers ))
):
    
    logger.info(f"Getting Total products")
    return( service.get_total_products() )

@router.post("/products/", response_model = schemas.BulkProductLoad )
def BulkProductsLoad( 
    products  : List[schemas.ProductCreate], 
    service : ProductService = Depends( get_product_service ),  
    current_user = Depends(RoleChecker( allow_viewers ))
):
    
    logger.info(f"Loading Bulk Data")
    return( service.create_bulk_products( data = products ) )

@router.get("/products-catalog", response_model = schemas.ProductsPage)
def GetProductsCatalog(
    offset: int = Query(default=0, ge=0, description="Number of items to skip"),
    limit: int = Query(default=100, ge=1, le=1000, description="Items per page (Max: 1000)"),
    service: ProductService = Depends(get_product_service),
    current_user = Depends(RoleChecker(allow_viewers))
):
    
    return service.get_all_products(
        offset = offset,
        limit = limit
    )
    