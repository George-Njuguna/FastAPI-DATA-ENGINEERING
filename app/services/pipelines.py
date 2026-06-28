from ..db import SessionLocal
from .. import models, schemas,crud

import io
import time
import pandas as pd
from sqlalchemy import insert, update
from fastapi import HTTPException , status 
from sqlalchemy.orm import Session
import logging
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FileIngestionService:

    @staticmethod
    def create_job_id(
        current_user: str,
        triggered_by: int
    ):
        
        job_id = str(uuid.uuid4())

        try:
            db = SessionLocal()

            crud.insert_jobs(
                db,
                job_id = job_id,
                triggered_by = triggered_by,
                job_status = models.Status.QUEUED
            )

            db.commit()

            return job_id

        except Exception as e:
            db.rollback()
            db.close()
            raise e
        
 
    @staticmethod
    def bulk_insert_csv_stream(
        cls, 
        file_bytes: bytes, 
        triggered_by: str, 
        job_id : str,
        db: Session = None, 
        chunk_size: int = 10000
        ):

        # Checking if Session db session has been loaded 
        is_independent_task = (db is None)

        if is_independent_task:

            db = SessionLocal() # this is for Asyncronised tasks
        
        try:

            crud.update_jobs(
                db = db,
                job_id = job_id,
                job_status = models.Status.PROCESSING
            )

            db.commit()

            # io.BytesIO turns raw bytes into a file-like object that Pandas can read
            file_wrapper = io.BytesIO(file_bytes)           
            # Read the CSV in manageable chunks (Memory-safe)
            # This ensures your server never uses more than a few MBs of RAM
            csv_reader = pd.read_csv(file_wrapper, chunksize=chunk_size)

            # NOTE : ALWAYS VALIDATE THE CSV FILE BEFORE INSERTING WITE A SCRIPT THAT CHECKS THE COLUMNS THAT ARE REQUIRED IF THEY ARE THERE 
            
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
                
            crud.update_jobs(
                db = db,
                job_id = job_id,
                job_status = models.Status.COMPLETED
            )
         
            db.commit()

            logger.info("INSERTING RECORDS")
 
            
        except Exception as e:
            db.rollback()

            crud.update_jobs(
                    db = db,
                    job_id = job_id,
                    job_status = models.Status.FAILED
                )
            db.commit()

            raise e
            
        finally:
            # closing the connection 
            if is_independent_task:
                logger.info("CLOSING THE CURRENT DATABASE CONNECTION")
                db.close()

        
    @staticmethod
    def demo_bulk_insert(
        job_id: str, 
        db: Session = None
    ):
        
        is_independent_task = (db is None)

        if is_independent_task:
            db = SessionLocal()
        try:
            crud.update_jobs(
                db = db,
                job_id = job_id,
                job_status = models.Status.PROCESSING
            )       

            db.commit() 

            total_inserted = 0

            for i in range(5000):
                total_inserted += 1

            time.sleep(300)

            crud.update_jobs(
                db = db,
                job_id = job_id,
                job_status = models.Status.COMPLETED
            )
            
            db.commit()
        
        except Exception as e:
            db.rollback()

            crud.update_jobs(
                    db = db,
                    job_id = job_id,
                    job_status = models.Status.FAILED
                )
            db.commit()

            raise e
            
        finally:
            if is_independent_task:
                logger.info("CLOSING THE CURRENT DATABASE CONNECTION")
                db.close()


    @staticmethod
    def get_job_status(
        id: str
    ):
        db = SessionLocal()
        job = crud.get_job_status( 
            db, 
            id 
        )
 
        if not job:
            raise HTTPException(
                status_code=404, 
                detail=f"job with ID {id} Not Found."
            )
        db.close()

        return job
            
                

        

   