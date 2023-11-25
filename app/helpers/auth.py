import json
from datetime import timedelta, datetime
from pathlib import Path
import os
import re
import jwt
import contextvars

import pytz
from cryptography.x509 import load_pem_x509_certificate
from dotenv import find_dotenv, load_dotenv
from jwt import (
    ExpiredSignatureError,
    ImmatureSignatureError,
    InvalidAlgorithmError,
    InvalidAudienceError,
    InvalidKeyError,
    InvalidSignatureError,
    InvalidTokenError,
    MissingRequiredClaimError,
)

from fastapi import Depends, HTTPException, APIRouter, Request, Body

from starlette import status
from starlette.requests import Request
from starlette.responses import Response, JSONResponse, HTMLResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from app import (
    context_external_user,
    context_external_user_token,
    context_user,
    global_external_user,
)
from app.helpers import api
from app.helpers.error import error_response
from app.helpers.api import request as api_request

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


class AuthorizeRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:

        # Paths to ignore
        paths_ignore = [
            "^\/$",
            "$\/beta$",
            "^\/app\/mobile",
            "^\/assets.*",
            "^\/favicon\.*",
            "^\/auth\/.*",
            "^\/\.well\-known.*",
        ]

        # Get URL Path
        path = request.url.path
        for key, val in request.path_params.items():
            path = path.replace(val, f"{{{key}}}", 1)

        # If session doesn't exist, continue
        if "auth_id_token" not in request.session:
            return await call_next(request)

        # If path is in one of the ignore items, continue
        for paths_ignore_item_re in paths_ignore:
            if re.search(paths_ignore_item_re, path):
                return await call_next(request)

        # Invoke refresh if token exists
        if "auth_time_expires" in request.session:
            datetime_auth_access_token_expiry = datetime.utcfromtimestamp(
                request.session["auth_time_expires"]
            )

            datetime_auth_access_token_issued = datetime.utcfromtimestamp(
                request.session["auth_time_issued"]
            )

            datetime_refresh_token_threshold = (
                datetime_auth_access_token_issued + timedelta(minutes=60)
            )

            # Advice from Auth0:
            # Set the token expiration to one week and refresh the token every time the user opens the web application and every one hour. If a user doesn't open the application for more than a week, they will have to login again and this is acceptable web application UX.

            if datetime.utcnow() > datetime_refresh_token_threshold:
                try:
                    client = api.get_client()
                    token = client.refresh_token(
                        f"https://{os.getenv('AUTH0_DOMAIN')}{os.getenv('AUTH0_ENDPOINT_TOKEN')}",
                        request.session["auth_refresh_token"],
                    )
                    request.session["auth_access_token"] = token["access_token"]
                    request.session["auth_refresh_token"] = token["refresh_token"]
                    request.session["auth_id_token"] = token["id_token"]
                    request.session["auth_scope"] = json.dumps(token["scope"])
                    request.session["auth_time_expires"] = token["expires_at"]
                    request.session["auth_time_issued"] = (
                        token["expires_at"] - token["expires_in"]
                    )

                except Exception as e:
                    return error_response(
                        request=request,
                        status_code=401,
                        detail="Couldn't refresh token, please login again",
                    )

        is_auth_token_id = True
        if request.session["auth_id_token"] is not None:
            auth_token = request.session["auth_id_token"]
            is_auth_token_id = True
        else:
            auth_token = request.session["auth_access_token"]
            is_auth_token_id = False

        # Don't try verifying/refreshing token if it's not there!

        try:
            token_payload = decode_and_validate_token(auth_token, is_auth_token_id)
        except (
            ExpiredSignatureError,
            ImmatureSignatureError,
            InvalidAlgorithmError,
            InvalidAudienceError,
            InvalidKeyError,
            InvalidSignatureError,
            InvalidTokenError,
            MissingRequiredClaimError,
        ) as error:

            # request.session['auth_id_token'] = None

            return error_response(request=request, status_code=401, detail=str(error))
            # return HTMLResponse(status_code=401, content=str(error))
        else:
            if "given_name" in token_payload:
                token_payload["name"] = (
                    token_payload["given_name"].strip()
                    + " "
                    + token_payload["family_name"].strip()
                )

            context_external_user.set(token_payload)
            context_external_user_token.set(auth_token)

        return await call_next(request)


def decode_and_validate_token(access_token, id_token=True):
    unverified_headers = jwt.get_unverified_header(access_token)
    public_key = load_pem_x509_certificate(
        (Path(__file__).parent / "../certs/auth0.pem").read_text().encode("utf-8")
    ).public_key()

    options = {
        "verify_exp": True,  # Skipping expiration date check
        "verify_aud": False,
    }

    if id_token:
        return jwt.decode(
            access_token,
            key=public_key,
            algorithms=unverified_headers["alg"],
            audience=os.getenv("AUTH0_AUDIENCE"),
        )
    else:
        return jwt.decode(
            access_token,
            key=public_key,
            algorithms=unverified_headers["alg"],
            audience=os.getenv("AUTH0_AUDIENCE"),
        )


def get_current_user(request: Request):

    # Check to see if user is already in context, if not check to see if auth_id_token is in session, else ret
    if context_user.get() is not None:
        user_api = context_user.get()
    else:
        if "auth_id_token" in request.session:
            user_api = api_request(url="/users/me")
            context_user.set(user_api)
        else:
            return None

    try:

        user_details = {
            "details": context_external_user.get(),
            "token": context_external_user_token.get(),
            "api": context_user.get(),
        }

        # Beta Testing Access Limitation HACK
        if (
            str(request.url).endswith("/beta") is False
            and user_api["features"].get("beta") is None
            and "@xero.com" not in user_api["email"]
        ):
            raise HTTPException(
                status_code=307, detail="Redirecting...", headers={"Location": "/beta"},
            )

        return user_details

    except LookupError as e:
        raise HTTPException(
            status_code=307, detail="Redirecting...", headers={"Location": "/"}
        )


def get_user_access(request: Request):

    if "auth_id_token" in request.session:
        return True
    else:
        raise HTTPException(
            status_code=307, detail="Redirecting...", headers={"Location": "/"}
        )


# https://whatsleft.au.auth0.com/authorize?
# scope=openid%20profile%20email
# response_type=token
# state=my-custom-state
# sso=false
# audience=https%3A%2F%2Fwhatsleft.nz%2Favailable-balance-app
# prompt=login
# client_id=B5TcPc6kX7thhmZD4iozXOsdgI93lqIl
# redirect_uri=https%3A%2F%2Fwhatsleft.au12.webtask.io%2Fauth0-authentication-api-debugger
# auth0Client=eyJuYW1lIjoiYXV0aDAuanMiLCJ2ZXJzaW9uIjoiNi44LjQifQ

# https://whatsleft.au.auth0.com/authorize?
# response_type=token
# client_id=B5TcPc6kX7thhmZD4iozXOsdgI93lqIl
# redirect_uri=https%3A%2F%2Flocalhost%3A7400%2Fauth%2Fcallback
# scope=openid+email+profile
# state=Q5QIQwrc32fTX4PPC06SUOdjCkUuU5
# prompt=login
# audience=https%3A%2F%2Fwhatsleft.nz%2Favailable-balance-app
