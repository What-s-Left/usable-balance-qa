import contextvars
import os
import json

from fastapi import Depends, HTTPException, APIRouter, Request, Body, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse

from xero_python.accounting import AccountingApi
from xero_python.api_client import ApiClient, serialize
from xero_python.api_client.configuration import Configuration
from xero_python.api_client.oauth2 import OAuth2Token
from xero_python.identity import IdentityApi

from app.helpers import data
from app.helpers.auth import get_current_user
from app.helpers.templates import templates
from app.helpers.api import request as api_request
from app.helpers.connection import xero_get_auth_url, xero_get_access_token, xero_access_token, xero_get_identities

router = APIRouter(
    prefix="/app/connection",
    tags=["app-connection"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/xero", response_class=HTMLResponse)
async def homepage(
    request: Request,
    user: dict = Depends(get_current_user)
):

    # Get Connection URL associated to user
    connection_url = xero_get_auth_url()

    return RedirectResponse(url=connection_url)


@router.get("/xero/callback", response_class=HTMLResponse)
async def homepage(
    request: Request,
    code: str,
    user: dict = Depends(get_current_user)
):

    # Got Code, now generate token, create/update entity and then setup a new connection with that token.
    access_token = xero_get_access_token(code=code)
    access_token = {'token': json.loads(access_token) }

    identities = xero_get_identities(access_token)

    for identity in identities:

        entity = {
            "id_src": f"XERO:{identity.id}",
            "name": identity.tenant_name,
            "src": data.to_json(identity)
        }

        entity = api_request(url="/entities", type="POST", data=entity)

        connection = {
            "name": identity.tenant_name,
            "id_src": f"XERO:{identity.id}",
            "type": "XERO",
            "entity_id": entity['id'],
            "token": json.dumps(data.to_json(access_token))
        }

        connection = api_request(url="/connections", type="POST", data=connection)

        entity = api_request(url="/entities", type="POST", data=entity)

    return RedirectResponse(url='/app')


