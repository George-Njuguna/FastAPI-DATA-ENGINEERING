from ..db import SessionLocal
from .. import models, schemas

import io
import pandas as pd
from sqlalchemy import insert
from sqlalchemy.orm import Session
import logging
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FileIngestionService:
   
    @staticmethod
    def bulk_insert_csv_stream(
        cls, 
        file_bytes: bytes, 
        triggered_by: str, 
        db: Session = None, 
        chunk_size: int = 10000
        ):

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
            logger.info("INSERTING RECORDS")
            return schemas.BulkResponse(
                status = "Queued" if is_independent_task else "sucessfully loaded",
                job_id = str(uuid.uuid4()),
                triggered_by = triggered_by,
            )
            
        except Exception as e:
            db.rollback()
            raise e
            
        finally:
            # closing the connection 
            if is_independent_task:
                logger.info("CLOSING THE CURRENT DATABASE CONNECTION")
                db.close()

   