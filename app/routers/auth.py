import json
import os
from datetime import datetime
from typing import Optional
from urllib import parse

from fastapi import Depends, HTTPException, APIRouter, Request, Body, Response, status
from fastapi.responses import RedirectResponse, JSONResponse, HTMLResponse

from app.helpers import api
from app.helpers.templates import templates

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


#@router.get("/", response_model=list[schemas.UserView])
#async def user_get_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#    users = crud.user_get_all(db, skip=skip, limit=limit)
#    return users


@router.get("/login", response_class=HTMLResponse)
async def auth_login(
    request: Request,
    state: Optional[str] = None,
    redirect: Optional[str] = None
):
    if state is not None:
        request.session['auth_state'] = state
        request.session['auth_redirect'] = redirect
        redirect_url = api.login(state=state)
        return RedirectResponse(redirect_url)
    else:
        # Get the client to set the state
        return templates.TemplateResponse("pages/auth/login.html", {"request": request})


@router.get("/callback", response_class=HTMLResponse)
async def auth_callback(
        request: Request,
        code: str
):

    token = api.token_get(code)
    request.session['auth_access_token'] = token['access_token']
    request.session['auth_id_token'] = token['id_token']
    request.session['auth_scope'] = json.dumps(token['scope'])
    request.session['auth_expires'] = datetime.fromtimestamp(token['expires_at']).strftime("%Y-%m-%d %H:%M:%S")

    #return RedirectResponse(request.session['auth_redirect'])
    return templates.TemplateResponse("pages/auth/callback.html", {"request": request})


@router.post("/callback", response_class=HTMLResponse)
async def auth_callback(
        request: Request
):

    #token = api.token_get(code)
    #return token

    request_body = await request.body()
    access_token = parse.parse_qs(request_body.decode("utf-8"))

    if access_token['state'] != request.session.get("auth_state"):
        raise HTTPException(status_code=401, detail="State Mismatch in Access Token")
    else:
        request.session['auth_token'] = access_token
        return RedirectResponse(request.session.get('auth_redirect'))

    #return templates.TemplateResponse("pages/auth/callback.html", {"request": request})


@router.get("/logout", response_class=HTMLResponse)
async def auth_logout(
    request: Request
):

    request.session.clear()
    return RedirectResponse("/")

