from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

SESSION_COOKIE_NAME = "session_id"

PUBLIC_PATHS = ["/auth/login", "/auth/register", "/static"]

# in minutes
TIME_TO_INACTIVATE = 15
SESSION_TTL = 30
