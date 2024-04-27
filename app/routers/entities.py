import contextvars
import os
import json
import re

from fastapi import Depends, HTTPException, APIRouter, Request, Body, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi_sqlalchemy import db
from fastapi.responses import JSONResponse

from helpers.ai.openai import wait_on_run
from helpers.auth.funcs import get_app_current_user, get_qa_current_user, get_qa_user_access
from helpers.data import crud, models, schemas
from helpers.generic.addresses import countries
from helpers.generic.data import get_value_from_key
from helpers.generic.secrets import get_secret
from helpers.generic.templates import templates
from helpers.generic import data as data_helper
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


@router.get("/match/api/feed", response_class=HTMLResponse)
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

    response = templates.TemplateResponse("partials/app/entities/match/search/feed.html", {
        "request": request,
        "user": user,
        "feed": feed
    })

    return response


@router.get("/match/api/entity", response_class=HTMLResponse)
async def entity_match_entity(
    request: Request,
    user: dict = Depends(get_qa_current_user),
    access: bool = Depends(get_qa_user_access),
):

    # Get entities associated to user
    entities = crud.entity_get_all(
        db=db.session,
        search={
            'name': request.query_params.get('name'),
        }
    )

    response = templates.TemplateResponse("partials/app/entities/match/search/entity.html", {
        "request": request,
        "user": user,
        "entities": entities
    })

    return response


@router.get("/match/api/ext-entity", response_class=HTMLResponse)
async def ext_entity_match_entity(
    request: Request,
    user: dict = Depends(get_qa_current_user),
    access: bool = Depends(get_qa_user_access),
):

    # Get entities associated to user
    entities = crud.ext_entity_get_all(
        db=db.session,
        search={
            'name': request.query_params.get('name'),
        }
    )

    response = templates.TemplateResponse("partials/app/entities/match/search/ext-entity.html", {
        "request": request,
        "user": user,
        "entities": entities
    })

    return response

@router.get("/match/api/ai", response_class=HTMLResponse)
async def ext_entity_match_entity_ai(
    request: Request,
    ext_entity_id: str,
    user: dict = Depends(get_qa_current_user),
    access: bool = Depends(get_qa_user_access),
):

    ext_entity = crud.ext_entity_get(db=db.session, ext_entity_id=ext_entity_id)

    from openai import OpenAI

    # Get entities associated to user

    client = OpenAI(api_key=get_secret("OPENAI_KEY"))

    thread = client.beta.threads.create()

    prompt_user = f"""
    
    Trading Names (if any): {", ".join(ext_entity.name)}
    
    Legal Name: {ext_entity.name_legal}
    
    Industry Description: {get_value_from_key(ext_entity.classification, "BIC", True)['desc']}
    
    Address: {get_value_from_key(ext_entity.identifier, "ADDRESS")} , { get_value_from_key(ext_entity.identifier, "POSTCODE")} 
    
    """

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt_user,
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=get_secret("OPENAI_ENTITY_ASSISTANT_ID"),
    )

    # Async call, so need to wait for it to finish
    result = wait_on_run(client, run, thread)

    messages = client.beta.threads.messages.list(thread_id=thread.id)

    response = templates.TemplateResponse("partials/app/entities/match/search/ai-entity.html", {
        "request": request,
        "user": user,
        "ext_entity": ext_entity,
        "ai_entity": messages
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
        "countries": countries,
        "classifications": {
            "expense": crud.account_get_all(db=db.session, classification="EXPENSE"),
            "revenue": crud.account_get_all(db=db.session, classification="REVENUE"),
        }
    })

    return response


@router.post("/new", response_class=HTMLResponse)
async def entities_create(
    request: Request,
    data: schemas.EntityCreate,
    user: dict = Depends(get_qa_current_user),
    access: bool = Depends(get_qa_user_access),
):

    entity = crud.entity_create(db=db.session, data=data)

    if request.headers.get("Content-Type") == "application/json":
        response = JSONResponse({
            "entity_id": data_helper.to_json(entity.id)
        })
    else:
        response = RedirectResponse(f"/app/entities/{entity.id}")

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
        "entity": entity,
        "transaction": transaction,
        "transaction_payee": transaction_payee,
        "transaction_reference": transaction_reference,
        "transaction_code": transaction_code,
        "countries": countries,
        "classifications": {
            "expense": crud.account_get_all(db=db.session, classification="EXPENSE"),
            "revenue": crud.account_get_all(db=db.session, classification="REVENUE"),
        }
    })

    return response


@router.post("/{entity_id}", response_class=HTMLResponse)
async def entities_update(
    request: Request,
    entity_id: str,
    data: schemas.EntityUpdate,
    user: dict = Depends(get_qa_current_user),
    access: bool = Depends(get_qa_user_access),
):

    entity = crud.entity_get(db=db.session, entity_id=entity_id)

    for feed in data.feed:
        entity.feed.append({
            'type': feed.get('type'),
            'value': re.escape(feed.get('value'))
        })

    entity = crud.entity_update(
        db=db.session,
        entity_id=entity_id,
        data=entity
    )

    if request.headers.get("Content-Type") == "application/json":
        response = JSONResponse({
            "entity_id": data_helper.to_json(entity.id)
        })
    else:
        response = RedirectResponse(f"/app/entities/{entity.id}")

    return response
