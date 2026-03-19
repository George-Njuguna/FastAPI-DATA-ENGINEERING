from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Data Engineering API is running"}



@app.post("/ingest")
def ingest_data():
    return {"status": "Data received successfully"}

