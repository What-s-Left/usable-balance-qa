import contextvars
import os
import json

from fastapi import Depends, HTTPException, APIRouter, Request, Body, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi_sqlalchemy import db

from helpers.auth.funcs import get_app_current_user, get_qa_current_user, get_qa_user_access
from helpers.data import crud
from helpers.generic.templates import templates
from helpers.app.api import request as api_request

router = APIRouter(
    prefix="/app/rules",
    tags=["app-rules"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_class=HTMLResponse)
async def rules_index(
    request: Request,
    page: int = 1,
    per_page: int = 25,
    search: str = None,
    user: dict = Depends(get_qa_current_user),
    access: bool = Depends(get_qa_user_access),
):

    # Get entities
    entities = crud.entity_get_all(
        db=db.session
    )

    response = templates.TemplateResponse("pages/app/transactions/index.html", {
        "request": request,
        "user": user,
        "entities": entities
    })

    return response


@router.get("/new", response_class=HTMLResponse)
async def rules_create(
    request: Request,
    user: dict = Depends(get_qa_current_user),
    access: bool = Depends(get_qa_user_access),
):

    response = templates.TemplateResponse("pages/app/entities/new.html", {
        "request": request,
        "user": user,
    })

    return response


@router.get("/{rule_id}", response_class=HTMLResponse)
async def rules_view(
    request: Request,
    rule_id: str,
    user: dict = Depends(get_qa_current_user),
    access: bool = Depends(get_qa_user_access),
):

    rule = crud.rule_get(db=db.session, rule_id=rule_id)

    response = templates.TemplateResponse("pages/app/entities/edit.html", {
        "request": request,
        "user": user,
        "rule": rule
    })

    return response


@router.post("/{entity_id}", response_class=HTMLResponse)
async def rules_edit(
    request: Request,
    rule_id: str,
    user: dict = Depends(get_qa_current_user),
    access: bool = Depends(get_qa_user_access),
):

    rule = crud.rule_get(db=db.session, rule_id=rule_id)

    response = templates.TemplateResponse("pages/app/entities/edit.html", {
        "request": request,
        "user": user,
        "rule": rule
    })

    return response
