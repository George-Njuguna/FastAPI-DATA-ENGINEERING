from fastapi import FastAPI
import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.get("/")
def root():
    return {
        "message": "Data Engineering API is running"
    }


@app.post("/ingest-customer")
def ingest_customer_data():
    logger.info("New data ingestion request received")
    return {
        "status": "Success",
        "message": "Customer data ingested"
    }

@app.get("/health")
def health_status():
    return{
        "status": "OK"
    }
    
