from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

# SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
# MONGO_URL = os.getenv("MONGO_URL")
# MONGO_DB = os.getenv("MONGO_DB")
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:root@localhost/tododb'
MONGO_URL = 'mongodb://localhost:27017'
MONGO_DB = 'logdb'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

mongo_client = AsyncIOMotorClient(MONGO_URL)
mongo_db = mongo_client[MONGO_DB]
