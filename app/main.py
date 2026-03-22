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

 # ingest endpoint
@app.post("/ingest-customer")
def ingest_customer_data():
    logger.info("New data ingestion request received")
    return {
        "status": "Success",
        "message": "Customer data ingested"
    }

 # Health endpoint
@app.get("/health")
def health_status():
    return{
        "status": "OK"
    }

 # Getting specific data 
@app.get("/customer/{customer_id}")
def customer_id_query(customer_id : int): # This requires the customer to have a specific datatype if you place 'abc' it is rejected automatically
    return{
        "customer_id" : customer_id,
        "Message" : "Customer Fetched Successfully"
    }

    
