from ..db import SessionLocal
from ..schemas import BulkResponse
from .. import models

import io
import pandas as pd
from sqlalchemy import insert
from sqlalchemy.orm import Session


class FileIngestionService:
   
    @staticmethod
    def bulk_insert_csv_stream(cls, file_bytes: bytes, db: Session = None, chunk_size: int = 10000):

        # Checking if Session db session has been loaded 
        is_independent_task = (db is None)

        if is_independent_task:

            db = SessionLocal() # this is for Asyncronised tasks
        
        try:
            # io.BytesIO turns raw bytes into a file-like object that Pandas can read
            file_wrapper = io.BytesIO(file_bytes)           
            # Read the CSV in manageable chunks (Memory-safe)
            # This ensures your server never uses more than a few MBs of RAM
            csv_reader = pd.read_csv(file_wrapper, chunksize=chunk_size)
            
            total_inserted = 0
            for chunk in csv_reader:
                # 1. Clean data or align headers if necessary
                # Convert the Pandas Dataframe chunk into a list of plain Python dictionaries
                records = chunk.to_dict(orient="records")
                
                if not records:
                    continue
                    
                # 2. Execute the professional high-speed batch insert
                db.execute(insert(models.Product), records)
                total_inserted += len(records)
                
            db.commit()
            return total_inserted
            
        except Exception as e:
            db.rollback()
            raise e
            
        finally:
            # closing the connection 
            if is_independent_task:
                db.close()

   