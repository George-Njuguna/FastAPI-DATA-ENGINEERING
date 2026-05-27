from .. import schemas, crud
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException , status

class ProductService:

    @staticmethod
    def create_product( db: Session, data: schemas.ProductCreate ):
        try:

            new_product = crud.add_product( db, data )
            
            db.flush() 
            db.commit()
            
            return new_product

        except Exception as e:

            db.rollback()
            raise e
    
    @staticmethod
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
        
    @staticmethod
    def get_total_products(db: Session , category : str | None = None ) -> int :

        count = crud.get_total_products(db)

        return schemas.ProductStats(
            total_count = count,
            category = category or "all",
            generated_at = datetime.now()
        )

    @staticmethod
    def get_product_by_id( db: Session, id: int ):

        product = crud.get_product_by_id( db, id )

        if not product:
            raise HTTPException(
                status_code=404, 
                detail=f"Product with ID {id} Not Found."
            )

        return product
