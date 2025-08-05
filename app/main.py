from fastapi import FastAPI
from lifespan import lifespan
from routers import auth

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
