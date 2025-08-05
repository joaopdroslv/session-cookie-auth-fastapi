from fastapi import FastAPI
from lifespan import lifespan
from routers import auth, home

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(home.router)
