from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from .models import Base, Request, Response

# Import configuration settings from config.py
from ..config import settings

# Create SQLAlchemy engine using the configured database URL
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,  # Use QueuePool for efficient connection management
    pool_size=10,  # Set the maximum number of connections in the pool
    max_overflow=20,  # Set the maximum number of connections allowed beyond the pool size
)

# Create a declarative base for defining database models
Base = declarative_base()

# Create a session factory to create database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define a function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create all database tables
Base.metadata.create_all(bind=engine)