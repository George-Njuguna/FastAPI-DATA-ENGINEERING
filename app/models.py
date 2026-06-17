from sqlalchemy import Column, Integer, String, Float, DateTime, Enum
from sqlalchemy.sql import func
import enum
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    ENGINEER = "engineer"
    ANALYST = "analyst"
    VIEWER = "viewer"

class Status(str, enum.Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class User(Base):
    __tablename__ = "users" 

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    created_at = Column(DateTime(timezone=True), server_default = func.now())

    role = Column(Enum(UserRole), default=UserRole.VIEWER, nullable = False)

class Product(Base):
    __tablename__ = "products" 

    id = Column(Integer, primary_key=True, index = True)
    sku = Column(String, unique=True, nullable=False)
    name = Column(String)
    details = Column(String)
    price = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class JobStatus(Base):
    __tablename__ = "jobs"

    job_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    status = Column(Enum(Status), default = Status.PROCESSING, nullable = False)
    triggered_by = Column(Integer)
    triggered_at = Column(DateTime(timezone = True), server_default = func.now())