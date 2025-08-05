from contextlib import asynccontextmanager

from database.database import Base, engine
from fastapi import FastAPI
from models.session import Session
from models.user import User


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")
    yield
