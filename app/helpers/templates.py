from datetime import datetime
from dateutil.parser import parse

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/html")


def today(input):
    """Custom filter"""
    return datetime.date.today().year


templates.env.globals["today"] = today


def format_datetime(datetime_str: str, format='medium'):
    datetime_obj = parse(datetime_str, fuzzy_with_tokens=True)
    if format == 'full':
        return datetime_obj[0].strftime("%d/%m/%Y, %H:%M:%S")
    else:
        return datetime_obj[0].strftime("%d/%m/%Y")


templates.env.filters["format_datetime"] = format_datetime