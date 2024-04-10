import contextvars
import os
import json

from fastapi import Depends, HTTPException, APIRouter, Request, Body, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse

from helpers.auth.funcs import get_app_current_user, get_qa_current_user, get_qa_user_access
from helpers.generic.templates import templates
from helpers.app.api import request as api_request

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
    user: dict = Depends(get_qa_current_user),
    access: bool = Depends(get_qa_user_access),
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



