import os
from datetime import datetime

from fastapi import Depends, HTTPException, APIRouter, Request, Body, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse

from helpers.auth.funcs import get_app_current_user, get_app_user_access, get_qa_current_user, get_qa_user_access
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
    user: dict = Depends(get_qa_current_user),
    access: bool = Depends(get_qa_user_access),
):

    response = templates.TemplateResponse("pages/app/index.html", {
        "request": request,
        "user": user,
    })

    return response



