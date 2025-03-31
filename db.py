from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from typing import Annotated
import os
from dotenv import load_dotenv

"""
alembic revision --autogenerate -m "Descripción de la actualización"
alembic upgrade head
alembic downgrade -1
"""

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
    
SessionDep = Annotated[Session, Depends(get_session)]