from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

SESSION_COOKIE_NAME = "session_id"
INACTIVITY_MINUTES = 15
SESSION_LIFESPAN_MINUTES = 30
