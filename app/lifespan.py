import time
from contextlib import asynccontextmanager

from database.database import Base, engine
from fastapi import FastAPI
from models.session import Session
from models.user import User
from sqlalchemy import text


@asynccontextmanager
async def lifespan(app: FastAPI):

    max_tries = 18  # 3 minutes of max waiting time
    wait_seconds = 10

    for attempt in range(max_tries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("Database is ready!")
            break

        except Exception as e:
            print(f"Database not ready yet (attempt {attempt + 1}/{max_tries}): {e}")
            time.sleep(wait_seconds)

    else:
        raise RuntimeError("Database did not become ready in time")

    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

    yield
