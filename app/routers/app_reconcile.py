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

router = APIRouter(
    prefix="/app/reconcile",
    tags=["app-reconcile"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/{entity_id}", response_class=HTMLResponse)
async def reconcile_entity(
    request: Request,
    entity_id: str,
    user: dict = Depends(get_current_user)
):

    # Get entity
    entity = api_request(url=f"/entities/{entity_id}")


    # Get entities associated to user
    reconcile = api_request(url=f"/entities/{entity_id}/reconcile?transactions=true")

    response = templates.TemplateResponse("pages/app/reconcile/index.html", {
        "request": request,
        "user": user,
        "entity": entity,
        "reconcile": reconcile
    })

    return response



