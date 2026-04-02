from fastapi import FastAPI
import logging
from pydantic import BaseModel, Field , EmailStr, field_validator
from datetime import datetime, timezone
from uuid import uuid4
from typing import List 

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
@app.get("/customers")
def customers(country : str , limit : int): # getting a certain number of customers based on country
    return{
        "country" : country,
        "limit" : limit, 
        "data" : []
    }
    
 # Request body (data given by the user to your Application)
 # First we create a class that inherits base model that will define the shape of our data 
class Product(BaseModel):
    id : str = Field(default_factory = lambda: str(uuid4())) # setting a dynamic default value that creates a new id everytime a new product is ingested
    created_at: datetime = Field(default_factory = lambda: datetime.now(timezone.utc)) # runs datetime.now() anytime there is a new instance 
    name : str
    price : int = Field(le = 5000 , gt = 0) # setting the price to be greater than 0 but less than 5000
    description : str | None = None  # setting the description as optional 
    in_stock : bool = True # Setting a constant default value

 # we will then use the model as a parameter 
@app.post("/ingest-product")
def insert_items(product : Product): 
    
    return {
        "status" : "success",
        "product" : product.model_dump() # you can return the pydantic model directly but it is usually advised to return a dictonary
    }

 # we will now create an order endpoint that has nested models
class Customer(BaseModel):
    name : str = Field(min_length = 2)
     # creating field validator for name 
    email : EmailStr
     # creating field validator to get lowercase emails 
    @field_validator("email")
    @classmethod
    def normalize_email(cls, v : str) -> str:
        return v.strip().lower() # changes the email to lowercase 


class Item(BaseModel):
    sku : str = Field(pattern=r"^[A-Z]{3}-\d+$")
    price : int = Field(gt = 0)

class Order(BaseModel):
    order_id : str = Field(default_factory = lambda: str(uuid4()))
    customer : Customer
    item : List[Item] = Field(min_length = 1) # ensuring the list is not empty 

@app.post("/orders")
def post_orders(order : Order):
    return {
        "message" : "sucessfully Loaded Orders",
        "order" : order.model_dump()
    }



@app.get("/product/{product-id}")
def get_product(product_id : int):# if a parameter exists it must be used in the output or logic
    return{
        "message" : "success",
        "product_id" : product_id
    }

@app.get("products")
def get_products(min_price : int = 1000 , max_price : int  = 5000): # if a parameter exists it must be used in the output or logic
    return{
        "message" : "success",
        "filters" : {
            "min_price" : min_price,
            "max_price" : max_price
        },
        "data" : []
    }
    

