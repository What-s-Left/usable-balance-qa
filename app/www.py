import datetime
from json import JSONDecodeError

from dotenv import find_dotenv, load_dotenv

from .config import config
from os import environ
import os
import contextvars

from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import sentry_sdk
from sentry_sdk.integrations.starlette import StarletteIntegration
from sentry_sdk.integrations.fastapi import FastApiIntegration

from app.routers import base, auth, app, app_reconcile
from app.helpers.templates import templates
from app.helpers.auth import AuthorizeRequestMiddleware
from app.helpers.error import error_response
from app.data.models import Session

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN_FASTAPI'),
    integrations=[
        StarletteIntegration(transaction_style="url"),
        FastApiIntegration(transaction_style="url"),
    ],
    traces_sample_rate=1.0,
)

#config = config.get(environ.get('FASTAPI_CONFIG') or 'default')


def include_router(www):
    www.include_router(base.router)
    www.include_router(auth.router)
    www.include_router(app.router)
    www.include_router(app_reconcile.router)


def mount_static(www):
    www.mount("/assets", StaticFiles(directory="app/assets"), name="assets")


def start_api():
    www = FastAPI(debug=True)

    # oas_doc = yaml.safe_load((Path(__file__).parent / "oas.yaml").read_text())
    # api.openapi = lambda: oas_doc

    #www.add_middleware(UserAccessModelRequestMiddleware)
    www.add_middleware(AuthorizeRequestMiddleware)
    www.add_middleware(
        SessionMiddleware,
        secret_key=os.getenv("APP_SECRET_KEY"),
        #same_site="none",
        https_only=True
    )

    www.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    include_router(www)
    mount_static(www)
    return www


www = start_api()


@www.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        # Log the exception here
        return error_response(
            request=request, status_code=500, detail=", ".join(exc.args)
        )


@www.exception_handler(Exception)
async def universal_exception_handler(request: Request, exc: Exception):
    # print(exc.status_code, exc.detail)

    return error_response(
        request=request, status_code=500, detail=", ".join(exc.args)
    )

@www.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    # print(exc.status_code, exc.detail)

    if exc.status_code in [301, 302, 303, 307]:
        return Response(
            status_code=exc.status_code, headers={"Location": exc.headers["Location"]}
        )
    else:
        return error_response(
            request=request, status_code=exc.status_code, detail=exc.detail
        )


@www.exception_handler(JSONDecodeError)
async def json_exception_handler(request: Request, exc: JSONDecodeError):
    # print(exc.status_code, exc.detail)

    return error_response(
        request=request, status_code="400", detail="API response not JSON"
    )