from ..db import SessionLocal
from ..schemas import BulkResponse
from .. import models

import io
import pandas as pd
from sqlalchemy import insert
from sqlalchemy.orm import Session


class FileIngestionService:

    
    @staticmethod
    def bulk_insert_csv_stream(db: Session, file_bytes: bytes, chunk_size: int = 10000):
        
        # io.BytesIO turns raw bytes into a file-like object that Pandas can read
        file_wrapper = io.BytesIO(file_bytes)
        
        try:
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
            print(f"[FILE INGESTION SUCCESS] Safely uploaded {total_inserted} rows.")
            return total_inserted
            
        except Exception as e:
            db.rollback()
            print(f"[FILE INGESTION CRASH] Data rolled back: {str(e)}")
            raise e

    @staticmethod
    def bulk_insert_json_stream(db: Session, file_bytes: bytes):
        """
        Reads raw JSON bytes, parses the array, and bulk-inserts the records.
        """
        file_wrapper = io.BytesIO(file_bytes)
        try:
            # Read JSON file straight into a dataframe
            df = pd.read_json(file_wrapper)
            records = df.to_dict(orient="records")
            
            if records:
                db.execute(insert(models.Product), records)
                db.commit()
                
            return len(records)
        except Exception as e:
            db.rollback()
            raise e
