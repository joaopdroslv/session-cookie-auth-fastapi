from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

API_PREFIX = "/api/v1"
FRONTEND_PREFIX = "/app"

PUBLIC_PATHS = [f"{FRONTEND_PREFIX}/login", f"{FRONTEND_PREFIX}/register"]

SESSION_COOKIE_NAME = "session_id"

# in minutes
TIME_TO_INACTIVATE = 15
SESSION_TTL = 30
