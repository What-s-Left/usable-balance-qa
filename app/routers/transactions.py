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
    prefix="/app/transactions",
    tags=["app-transactions"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_class=HTMLResponse)
async def reconcile_entity(
    request: Request,
    page: int = 1,
    per_page: int = 25,
    search: str = None,
    user: dict = Depends(get_qa_current_user),
    access: bool = Depends(get_qa_user_access),
):

    # Get entities associated to user
    transactions = crud.transaction_get_all(
        db=db.session,
        page=page,
        per_page=per_page,
        search=search
    )

    response = templates.TemplateResponse("pages/app/transactions/index.html", {
        "request": request,
        "user": user,
        "page": page,
        "per_page": per_page,
        "search": search,
        "transactions": transactions
    })

    return response



