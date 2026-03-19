from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {
        "message": "Data Engineering API is running"
    }


@app.post("/ingest-customer")
def ingest_customer_data():
    return {
        "status": "Sucess",
        "message": "Customer data ingested"
    }

@app.get("/health")
def health_status():
    return{
        "status": "Ok"
    }
