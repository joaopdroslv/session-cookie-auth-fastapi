from fastapi import FastAPI, Request, Response, Form
from fastapi.responses import HTMLResponse


app = FastAPI()


@app.get("/login", response_class=HTMLResponse)
def login_page():

    return """
    <form action="/login" method="POST">
        E-mail: <input type="text" name="email" /><br/>
        Password: <input type="password" name="password" /><br/>
        <button type="submit">Login</button>
    </form>
    """


@app.post("/login")
def login(request: Request, response: Response, email: str = Form(...), password: str = Form(...)):

    print(request.__dict__)
    print(response.__dict__)
    print(email)
    print(password)
