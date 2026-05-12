from sqlalchemy import Column, Integer, String, Float,DateTime
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users" 

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Product(Base):
    __tablename__ = "products" 

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String)
    name = Column(String)
    details = Column(String)
    price = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())