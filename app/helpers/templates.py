import datetime

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/html")


def today(input):
    """Custom filter"""
    return datetime.date.today().year


templates.env.globals["today"] = today