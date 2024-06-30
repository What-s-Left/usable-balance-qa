import contextvars
import os
import json

from fastapi import Depends, HTTPException, APIRouter, Request, Body, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi_sqlalchemy import db

from helpers.auth.funcs import get_app_current_user, get_qa_current_user, get_qa_user_access
from helpers.data import crud
from helpers.generic.templates import render
from helpers.app.api import request as api_request

router = APIRouter(
    prefix="/app/messages",
    tags=["app-messages"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_class=HTMLResponse)
async def get_messages(
    request: Request,
    status: str = "UNREAD",
    datetime_from: str = None,
    datetime_to: str = None,
    page: int = 1,
    per_page: int = 25,
    search: str = None,
    user: dict = Depends(get_qa_current_user),
    access: bool = Depends(get_qa_user_access),
):

    # Get entities associated to user
    messages = crud.message_get_all(
        db=db.session,
        entity_id="UB:BASE",
        status=status,
        date_from=datetime_from,
        date_to=datetime_to
    )

    response = render("pages/app/messages/index.html", {
        "request": request,
        "user": user,
        "page": page,
        "per_page": per_page,
        "search": search,
        "status": status,
        "messages": messages
    })

    return response



