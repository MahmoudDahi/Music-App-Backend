from tracemalloc import start
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import TEXT, VARCHAR, Column, LargeBinary,create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import uuid
import bcrypt



# Using SQLAlchemy recommended URL format for PostgreSQL
DATABASE_URL = 'postgresql://postgres:md1234@localhost:5432/musicapp'

# Create database engine with connection pooling and logging
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False,bind=engine)
db = SessionLocal()

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(TEXT,primary_key=True)
    name = Column(VARCHAR(100))
    email = Column(VARCHAR(100))
    password = Column(LargeBinary)


class UserCreate(BaseModel):
    name:str
    email:str
    password:str


app = FastAPI()


Base.metadata.create_all(engine)