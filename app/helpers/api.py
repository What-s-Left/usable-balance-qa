import os
from distutils.util import strtobool
from typing import Optional
from urllib.parse import urlencode
import string
import random
import requests

from oauthlib.oauth2 import TokenExpiredError, MobileApplicationClient, WebApplicationClient
from requests_oauthlib import OAuth2Session
from auth0.v3.authentication.token_verifier import TokenVerifier, AsymmetricSignatureVerifier
from starlette.responses import RedirectResponse

from app import context_external_user, context_external_user_token


def get_client(token: Optional[str] = None):

    token_endpoint_url = f"https://{os.getenv('AUTH0_DOMAIN')}{os.getenv('AUTH0_ENDPOINT_TOKEN')}"

    client_token = MobileApplicationClient(
        client_id=os.getenv("AUTH0_CLIENT_ID")
    )

    client_token = WebApplicationClient(
        client_id=os.getenv("AUTH0_CLIENT_ID")
    )

    auth0 = OAuth2Session(
        client=client_token,
        scope="openid email profile",
        redirect_uri=os.getenv("AUTH0_CALLBACK"),
        token=token,
        auto_refresh_url=token_endpoint_url,
        auto_refresh_kwargs={
            "client_id": os.getenv("AUTH0_CLIENT_ID"),
            "client_secret": os.getenv("AUTH0_CLIENT_SECRET")
        },
        token_updater=token_save
    )

    return auth0


def login(callback=None, state=None):

    client = get_client()
    auth_endpoint_url = f"https://{os.getenv('AUTH0_DOMAIN')}{os.getenv('AUTH0_ENDPOINT_AUTH')}"
    authorization_url, state = client.authorization_url(
        auth_endpoint_url,
        state=state,
        prompt="login",
        #response_mode="form_post",
        audience=os.getenv('AUTH0_AUDIENCE')
    )

    return authorization_url


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
    ssl_verify = bool(strtobool(os.getenv("AB_API_SSL_VERIFY")))

    url_full = os.getenv("AB_API_BASE") + url

    try:
        if type == "GET":
            response = requests.get(url=url_full, verify=ssl_verify, headers=headers)
        else:
            response = requests.post(url=url_full, verify=ssl_verify, json=data, headers=headers)

        return response.json()

    except requests.exceptions.ConnectionError as e:
        RedirectResponse("/error")

    except requests.exceptions.HTTPError as e:
    #except TokenExpiredError as e:
        token = token_refresh(token=token)
        return request(url=url, token=token, type=type, data=data)


def logout(callback: str):

    return callback
