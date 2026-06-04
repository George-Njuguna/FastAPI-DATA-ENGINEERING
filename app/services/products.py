from .. import schemas, crud
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException , status 

class ProductService:

    def __init__( 
            self,
            db : Session 
        ):
        
        self.db = db

    def create_product( 
            self, 
            data: schemas.ProductCreate 
        ):

        try:

            new_product = crud.add_product( 
                self.db, 
                data 
            )
            
            self.db.flush() 
            self.db.commit()
            
            return new_product

        except Exception as e:

            self.db.rollback()
            raise e
    
    def create_bulk_products( 
            self,
            data : list[schemas.ProductCreate] 
        ):

        try:

            crud.add_product_bulk( 
                self.db,
                data
            )

            self.db.commit()

            return {
                "inserted": len(data),
                "status": "success"
            }
        
        except Exception as e:

            self.db.rollback()
            raise e   
        
    def get_total_products( 
            self , 
            category : str | None = None 
        ) -> int :

        count = crud.get_total_products(
            self.db
        )

        return schemas.ProductStats(
            total_count = count,
            category = category or "all",
            generated_at = datetime.now()
        )

    def get_product_by_id( 
            self,
            id: int
        ):

        product = crud.get_product_by_id( 
            self.db, 
            id 
        )

        if not product:
            raise HTTPException(
                status_code=404, 
                detail=f"Product with ID {id} Not Found."
            )

        return product
