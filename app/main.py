from fastapi import FastAPI
import logging
from pydantic import BaseModel
from typing import Optional

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

 # Query Parameters.
@app.get("/customer")
def customers(country : str , limit : int): # getting a certain number of customers based on country
    return{
        "country" : country,
        "limit" : limit, 
        "data" : []
    }
    
 # Request body (data given by the user to your Application)
# First we create a class that inherits base model that will define the shape of our data 
class Product(BaseModel):
    name : str
    price : int
    in_stock : bool

# we will then use the model as a parameter 
@app.post("/ingest-product")
def insert_items(Product : Product):
    
    return {
        "status" : "success",
        "product" : Product
    }

@app.get("/product/{product_id}")
def get_product(product_id : int):
    return{
        "Message" : "Sucess",
        "Product" : []
    }

@app.get("products")
def get_products(min_price : int = 1000 , max_price = 5000):
    return{
        "Message" : "Sucess",
        "Data" : []
    }
    

