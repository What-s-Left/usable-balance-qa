import os
from datetime import datetime

from fastapi import Depends, HTTPException, APIRouter, Request, Body, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse

from helpers.app.auth import get_current_user
from helpers.generic.templates import templates
from helpers.app.api import request as api_request

router = APIRouter(
    prefix="/app",
    tags=["app"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


#@router.get("/", response_model=list[schemas.UserView])
#async def user_get_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#    users = crud.user_get_all(db, skip=skip, limit=limit)
#    return users


@router.get("/", response_class=HTMLResponse)
async def homepage(
    request: Request,
    user: dict = Depends(get_current_user)
):

    # Get entities associated to user
    entities = api_request(url="/entities")

    for idx, entity in enumerate(entities):
        entity_balance = api_request(url=f"/entities/{entity['id']}/balance")
        if entity_balance['datetime_transaction_latest']:
            entity_balance['datetime_transaction_latest'] = datetime.strptime(entity_balance['datetime_transaction_latest'], "%Y-%m-%dT%H:%M:%S")
        entities[idx]['balance'] = entity_balance

        entity_status = api_request(url=f"/entities/{entity['id']}/status")
        entities[idx]['status'] = entity_status

        entity['type'] = "BANK"
        if "XERO" in entity['id_src']:
            entity['type'] = "XERO"
        elif "MYOB" in entity['id_src']:
            entity['type'] = "MYOB"

    response = templates.TemplateResponse("pages/app/index.html", {
        "request": request,
        "user": user,
        "entities": entities
    })

    return response



