import os
import re
import datetime
import asyncio
import json
import contextvars
import logging

from auth0.v3.authentication import Users
from authlib.integrations.starlette_client import OAuth
from rauth import OAuth2Service

import xero_python
from xero_python.exceptions import http_status_exceptions
from xero_python.accounting import AccountingApi
from xero_python.api_client import ApiClient, serialize
from xero_python.api_client.configuration import Configuration
from xero_python.api_client.oauth2 import OAuth2Token
from xero_python.identity import IdentityApi


xero_access_token = contextvars.ContextVar("xero_access_token")

xero_api_oauth = OAuth2Service(
    name="xero",
    client_id=os.environ["CONNECTOR_XERO_CLIENT_ID"],
    client_secret=os.environ["CONNECTOR_XERO_CLIENT_SECRET"],
    base_url="https://api.xero.com/v2/",
    authorize_url="https://login.xero.com/identity/connect/authorize",
    access_token_url="https://identity.xero.com/connect/token",
)


def xero_get_auth_url():
    #redirect_url = request.url_for("connection_xero_callback")
    params = {
        'redirect_uri': os.environ["CONNECTOR_XERO_CALLBACK_URL"],
        'response_type': 'code',
        'scope': "offline_access accounting.transactions accounting.reports.read accounting.journals.read accounting.settings accounting.contacts",
    }

    auth_url = xero_api_oauth.get_authorize_url(**params)

    return auth_url


def xero_get_access_token(code: str):
    #redirect_url = request.url_for("connection_xero_callback")
    data = {
        'code': code,
        'grant_type': 'authorization_code',
        'client_secret': os.environ["CONNECTOR_XERO_CLIENT_SECRET"],
        'redirect_uri': os.environ["CONNECTOR_XERO_CALLBACK_URL"]
    }

    session = xero_api_oauth.get_raw_access_token(data=data)

    return str(session.content.decode())


def xero_get_identities(access_token: str):

    api_client = ApiClient(
        Configuration(
            oauth2_token=OAuth2Token(
                client_id=os.environ["CONNECTOR_XERO_CLIENT_ID"],
                client_secret=os.environ["CONNECTOR_XERO_CLIENT_SECRET"]
            )
        ),
        pool_threads=4,
    )

    @api_client.oauth2_token_getter
    def obtain_xero_oauth2_token():
        return json.loads(xero_access_token.get())

    @api_client.oauth2_token_saver
    def store_xero_oauth2_token(access_token):
        xero_access_token.set(json.dumps(access_token))

    api_client.set_oauth2_token(access_token['token'])

    api_accounting = AccountingApi(api_client)
    api_identity = IdentityApi(api_client)

    identities = []

    api_connections = api_identity.get_connections()

    if api_connections is not None:
        for api_connection in api_connections:
            if api_connection.tenant_type == "ORGANISATION":
                identities.append(api_connection)

    return identities
