import logs
from fastapi import FastAPI
from lifespan import lifespan
from middlewares.session import SessionMiddleware
from routers import auth, home

app = FastAPI(lifespan=lifespan)

app.add_middleware(SessionMiddleware)

app.include_router(auth.router)
app.include_router(home.router)
