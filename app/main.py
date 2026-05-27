from fastapi import FastAPI ,HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
import logging
from typing import List
from sqlalchemy.orm import Session
from . import schemas, db, services, auth
from .routers import auth, pipelines, products, users


app = FastAPI( title = "Data Engineering with Fast API" )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Connect the Department Routers to the Main Building
app.include_router(auth.router, prefix="/api/v1")
app.include_router(products.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")

@app.get("/")
def health_check():
    return {"status": "healthy", "environment": "production"}




