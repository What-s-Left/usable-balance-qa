import os

from fastapi import Depends, HTTPException, APIRouter, Request, Body, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.responses import JSONResponse

from helpers.generic.templates import templates

router = APIRouter(
    tags=["base"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


#@router.get("/", response_model=list[schemas.UserView])
#async def user_get_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#    users = crud.user_get_all(db, skip=skip, limit=limit)
#    return users


@router.get("/", response_class=HTMLResponse)
async def homepage(
    request: Request
):
    response = templates.TemplateResponse("pages/index.html", {"request": request})
    return response


@router.get("/.well-known/microsoft-identity-association.json", response_class=JSONResponse)
async def about(
    request: Request
):

    response = {
        "associatedApplications": [
            {
                "applicationId": "231708b0-1b2b-4224-9db2-d1f8a89d08b0"
            }
        ]
    }

    return JSONResponse(content=response)





