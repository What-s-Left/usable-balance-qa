import os
from distutils.util import strtobool
from typing import Optional
from urllib.parse import urlencode
import string
import random
import requests
from fastapi import HTTPException

from authlib.integrations.starlette_client import OAuth, OAuthError
from starlette.responses import RedirectResponse
from fastapi import FastAPI, Depends, HTTPException, status, Request

from app import context_external_user, context_external_user_token


def get_client(token: Optional[str] = None):
    oauth = OAuth()

    oauth.register(
        name='auth0',
        client_id=os.getenv("AUTH0_CLIENT_ID"),
        client_secret=os.getenv("AUTH0_CLIENT_SECRET"),
        authorize_url=f"https://{os.getenv('AUTH0_DOMAIN')}{os.getenv('AUTH0_ENDPOINT_AUTH')}",
        authorize_params=None,
        access_token_url=f"https://{os.getenv('AUTH0_DOMAIN')}{os.getenv('AUTH0_ENDPOINT_TOKEN')}",
        redirect_uri=os.getenv("AUTH0_CALLBACK"),
        client_kwargs={
            'scope': 'openid profile email'
        },
        server_metadata_url=os.getenv('AUTH0_CONF')
    )

    return oauth


def get_jwks_keys():
    metadata_url = os.getenv('AUTH0_KEYS')
    metadata = requests.get(metadata_url).json()
    jwks_keys = metadata.get("jwks_uri")
    return jwks_keys


def login(callback=None):
    redirect_uri = os.getenv("AUTH0_CALLBACK")
    return redirect_uri

    """
    client = get_client()
    auth_endpoint_url = f"https://{os.getenv('AUTH0_DOMAIN')}{os.getenv('AUTH0_ENDPOINT_AUTH')}"
    authorization_url, state = client.authorization_url(
        auth_endpoint_url,
        state=state,
        prompt="login",
        # response_mode="form_post",
        audience=os.getenv('AUTH0_AUDIENCE')
    )

    return authorization_url
    """


def token_get(code: str):
    client = get_client()
    token_endpoint_url = f"https://{os.getenv('AUTH0_DOMAIN')}{os.getenv('AUTH0_ENDPOINT_TOKEN')}"
    token = client.fetch_token(
        token_url=token_endpoint_url,
        client_secret=os.getenv('AUTH0_CLIENT_SECRET'),
        code=code
    )

    return token


def token_refresh(refresh_token: str):
    client = get_client()
    token_endpoint_url = f"https://{os.getenv('AUTH0_DOMAIN')}{os.getenv('AUTH0_ENDPOINT_TOKEN')}"
    token = client.refresh_token(
        token_url=token_endpoint_url,
        refresh_token=refresh_token
    )

    return token


def token_save(token: str):
    print(token)


def request(url: str, type: Optional[str] = "GET", data: Optional[dict] = {}):
    token = context_external_user_token.get()
    headers = {"Authorization": f"Bearer {token}"}
    ssl_verify = bool(strtobool(os.getenv("UB_API_SSL_VERIFY")))

    url_full = os.getenv("UB_API_BASE") + url

    try:
        if type == "GET":
            response = requests.get(url=url_full, verify=ssl_verify, headers=headers)
        else:
            response = requests.post(url=url_full, verify=ssl_verify, json=data, headers=headers)

        return response.json()

    except requests.exceptions.ConnectionError as e:
        raise HTTPException(status_code=500, detail="API isn't responding")

    except requests.exceptions.HTTPError as e:
        # except TokenExpiredError as e:
        token = token_refresh(token=token)
        return request(url=url, token=token, type=type, data=data)


def logout(callback: str):
    return callback
