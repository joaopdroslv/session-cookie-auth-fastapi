import logs
from config import API_PREFIX
from fastapi import FastAPI
from lifespan import lifespan
from middlewares.session import SessionMiddleware
from routers import auth, frontend

app = FastAPI(lifespan=lifespan)

app.add_middleware(SessionMiddleware)

app.include_router(auth.router, prefix=API_PREFIX)
app.include_router(frontend.router)
