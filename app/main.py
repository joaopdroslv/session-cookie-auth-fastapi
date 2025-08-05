from fastapi import FastAPI, Form, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from lifespan import lifespan

app = FastAPI(lifespan=lifespan)

templates = Jinja2Templates(directory="templates")


@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):

    return templates.TemplateResponse("auth/register.html", {"request": request})


@app.post("/register")
async def register(
    request: Request,
    response: Response,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
):

    print(name)
    print(email)
    print(password)
    print(confirm_password)


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):

    return templates.TemplateResponse("auth/login.html", {"request": request})


@app.post("/login")
def login(
    request: Request,
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
):

    print(email)
    print(password)
