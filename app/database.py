from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()



DB_URL = os.getenv("DB_URL")
if DB_URL is None:
    raise ValueError("DB_URL environment variable is not set")

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close

Base = declarative_base()


