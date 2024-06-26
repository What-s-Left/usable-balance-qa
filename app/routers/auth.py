import json
import os
from datetime import datetime
from typing import Optional
from urllib import parse

import jwt
from fastapi import Depends, HTTPException, APIRouter, Request, Body, Response, status
from fastapi.responses import RedirectResponse, JSONResponse, HTMLResponse

from helpers.app import api
from helpers.generic.secrets import get_secret
from helpers.generic.templates import render

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


# @router.get("/", response_model=list[schemas.UserView])
# async def user_get_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#    users = crud.user_get_all(db, skip=skip, limit=limit)
#    return users


@router.get("/login", response_class=HTMLResponse)
async def auth_login(
    request: Request,
    state: Optional[str] = None,
    redirect: Optional[str] = None,
    timezone: Optional[str] = None,
):
    client = api.get_client()

    if state is not None:
        request.session["auth_state"] = state
        request.session["auth_redirect"] = redirect
        request.session["timezone"] = timezone
        uri_redirect = api.login()
        uri_authorisation = client.create_authorization_url(
            url=f"https://{get_secret('AUTH0_DOMAIN')}{get_secret('AUTH0_ENDPOINT_AUTH')}",
            redirect_uri=uri_redirect,
            state=state,
            scope=get_secret("AUTH0_SCOPE")
        )
        return RedirectResponse(uri_authorisation[0], status_code=302)
    else:
        # Get the client to set the state
        return render("pages/auth/login.html", {"request": request})


@router.get("/login/xero", response_class=HTMLResponse)
async def auth_login_xero(
    request: Request,
    state: Optional[str] = None,
    redirect: Optional[str] = None,
    timezone: Optional[str] = None,
):
    client = api.get_client()

    if state is not None:
        request.session["auth_state"] = state
        request.session["auth_redirect"] = redirect
        request.session["timezone"] = timezone
        uri_redirect = api.login()
        uri_authorisation = client.create_authorization_url(
            url=f"https://{get_secret('AUTH0_DOMAIN')}{get_secret('AUTH0_ENDPOINT_AUTH')}",
            redirect_uri=uri_redirect,
            state=state,
            scope=get_secret("AUTH0_SCOPE"),
        )
        uri_authorisation_full = uri_authorisation[0] + "&connection=Xero"
        return RedirectResponse(uri_authorisation_full, status_code=302)
    else:
        # Get the client to set the state
        return render("pages/auth/login.html", {"request": request})


@router.get("/callback", response_class=HTMLResponse)
async def auth_callback(request: Request, code: str):
    state_from_session = request.session.get("auth_state")
    state_from_callback = request.query_params.get("state")
    if not state_from_session or state_from_callback != state_from_callback:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid state parameter"
        )

    client = api.get_client()

    try:
        token = client.fetch_token(
            f"https://{get_secret('AUTH0_DOMAIN')}{get_secret('AUTH0_ENDPOINT_TOKEN')}",
            code=code,
            client_secret=get_secret("AUTH0_CLIENT_SECRET"),
            redirect_uri=api.login(),
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to fetch access token",
        )

    request.session["auth_access_token"] = token["access_token"]
    request.session["auth_refresh_token"] = token["refresh_token"]
    request.session["auth_id_token"] = token["id_token"]
    request.session["auth_scope"] = json.dumps(token["scope"])
    request.session["auth_time_expires"] = token["expires_at"]
    request.session["auth_time_issued"] = token["expires_at"] - token["expires_in"]

    # return RedirectResponse(request.session['auth_redirect'])
    return render(
        "pages/auth/callback.html", {"request": request, "env": get_secret}
    )


@router.post("/callback", response_class=HTMLResponse)
async def auth_callback(request: Request):
    # token = api.token_get(code)
    # return token

    request_body = await request.body()
    access_token = parse.parse_qs(request_body.decode("utf-8"))

    if access_token["state"] != request.session.get("auth_state"):
        raise HTTPException(status_code=401, detail="State Mismatch in Access Token")
    else:
        request.session["auth_token"] = access_token
        return RedirectResponse(request.session.get("auth_redirect"))

    # return render("pages/auth/callback.html", {"request": request})


@router.get("/logout", response_class=HTMLResponse)
async def auth_logout(request: Request):
    redirect_logout = parse.quote(f"{get_secret('UB_WWW_BASE')}/logged-out", safe="")
    request.session.clear()
    redirect_uri = f"https://{get_secret('AUTH0_DOMAIN')}/v2/logout?returnTo={redirect_logout}&client_id={get_secret('AUTH0_CLIENT_ID')}"
    return RedirectResponse(redirect_uri)
