from pathlib import Path
import os
import re
import jwt
import contextvars

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

from auth0.v3.authentication import Users

from app import context_external_user, context_external_user_token
from app.helpers.error import error_response

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


class AuthorizeRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:

        # Paths to ignore
        paths_ignore = [
            '^\/$',
            '^\/assets.*',
            '^\/favicon\.ico',
            '^\/auth\/.*',
            '^\/\.well\-known.*'
        ]

        # Get URL Path
        path = request.url.path
        for key, val in request.path_params.items():
            path = path.replace(val, F'{{{key}}}', 1)

        # If session doesn't exist, continue
        if 'auth_id_token' not in request.session:
            return await call_next(request)

        # If path is in one of the ignore items, continue
        for paths_ignore_item_re in paths_ignore:
            if re.search(paths_ignore_item_re, path):
                return await call_next(request)

        auth_token = request.session['auth_id_token']

        # Don't try verifying/refreshing token if it's not there!


        try:
            token_payload = decode_and_validate_token(auth_token)
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

            request.session['auth_id_token'] = None

            return error_response(
                request=request,
                status_code=401,
                detail=str(error)
            )
            #return HTMLResponse(status_code=401, content=str(error))
        else:
            context_external_user.set(token_payload)
            context_external_user_token.set(auth_token)

        return await call_next(request)


def decode_and_validate_token(access_token):
    unverified_headers = jwt.get_unverified_header(access_token)
    public_key = load_pem_x509_certificate(
        (Path(__file__).parent / "../certs/auth0.pem").read_text().encode("utf-8")
    ).public_key()

    options = {
        'verify_exp': False,  # Skipping expiration date check
        'verify_aud': False
    }

    return jwt.decode(
        access_token,
        key=public_key,
        algorithms=unverified_headers["alg"],
        audience=os.getenv('AUTH0_AUDIENCE_TOKEN'),
    )


def get_current_user(request: Request):
    # TODO: Query API for user details here
    
    return {
        'details': context_external_user.get(),
        'token': context_external_user_token.get()
    }

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