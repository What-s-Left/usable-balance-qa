import contextvars
import os
import json

from fastapi import Depends, HTTPException, APIRouter, Request, Body, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi_sqlalchemy import db

from helpers.auth.funcs import get_app_current_user, get_qa_current_user, get_qa_user_access
from helpers.data import crud, models
from helpers.generic.templates import templates
from helpers.app.api import request as api_request

router = APIRouter(
    prefix="/app/entities",
    tags=["app-entities"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_class=HTMLResponse)
async def entities_index(
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


@router.get("/match/feed", response_class=HTMLResponse)
async def entity_match_feed(
    request: Request,
    user: dict = Depends(get_qa_current_user),
    access: bool = Depends(get_qa_user_access),
):

    # Get entities associated to user
    feed = crud.feed_get_all(
        db=db.session,
        search={
            'payee': request.query_params.get('payee'),
            'reference': request.query_params.get('reference'),
            'code': request.query_params.get('code')
        }
    )

    response = templates.TemplateResponse("partials/app/entities/match/feed.html", {
        "request": request,
        "user": user,
        "feed": feed
    })

    return response


@router.get("/match", response_class=HTMLResponse)
async def entities_match(
    request: Request,
    user: dict = Depends(get_qa_current_user),
    access: bool = Depends(get_qa_user_access),
):

    transaction = None
    transaction_id = request.query_params.get('transaction_id')

    transaction_payee = request.query_params.get('payee')
    transaction_reference = request.query_params.get('reference')
    transaction_code = request.query_params.get('code')

    if transaction_id:
        transaction = db.session.get(models.Transaction, transaction_id)

    response = templates.TemplateResponse("pages/app/entities/match.html", {
        "request": request,
        "user": user,
        "transaction": transaction,
        "transaction_payee": transaction_payee,
        "transaction_reference": transaction_reference,
        "transaction_code": transaction_code,
    })

    return response


@router.get("/new", response_class=HTMLResponse)
async def entities_new(
    request: Request,
    user: dict = Depends(get_qa_current_user),
    access: bool = Depends(get_qa_user_access),
):

    transaction = None
    transaction_id = request.query_params.get('transaction_id')

    transaction_payee = request.query_params.get('payee')
    transaction_reference = request.query_params.get('reference')
    transaction_code = request.query_params.get('code')

    if transaction_id:
        transaction = db.session.get(models.Transaction, transaction_id)

    response = templates.TemplateResponse("pages/app/entities/entity.html", {
        "request": request,
        "user": user,
        "transaction": transaction,
        "transaction_payee": transaction_payee,
        "transaction_reference": transaction_reference,
        "transaction_code": transaction_code,
    })

    return response


@router.get("/{entity_id}", response_class=HTMLResponse)
async def entities_view(
    request: Request,
    entity_id: str,
    user: dict = Depends(get_qa_current_user),
    access: bool = Depends(get_qa_user_access),
):

    entity = crud.entity_get(db=db.session, entity_id=entity_id)

    transaction = None
    transaction_id = request.query_params.get('transaction_id')

    transaction_payee = request.query_params.get('payee')
    transaction_reference = request.query_params.get('reference')
    transaction_code = request.query_params.get('code')

    if transaction_id:
        transaction = db.session.get(models.Transaction, transaction_id)

    response = templates.TemplateResponse("pages/app/entities/entity.html", {
        "request": request,
        "user": user,
        "transaction": transaction,
        "transaction_payee": transaction_payee,
        "transaction_reference": transaction_reference,
        "transaction_code": transaction_code,
    })

    response = templates.TemplateResponse("pages/app/entities/entity.html", {
        "request": request,
        "user": user,
        "entity": entity
    })

    return response


@router.post("/{entity_id}", response_class=HTMLResponse)
async def entities_update(
    request: Request,
    entity_id: str,
    user: dict = Depends(get_qa_current_user),
    access: bool = Depends(get_qa_user_access),
):

    entity = crud.entity_get(db=db.session, entity_id=entity_id)

    response = templates.TemplateResponse("pages/app/entities/edit.html", {
        "request": request,
        "user": user,
        "entity": entity
    })

    return response
