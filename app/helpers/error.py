from fastapi import FastAPI, Request, Depends

from app.helpers.templates import templates


def error_response(request: Request, status_code: None, detail: None):

    if status_code == 404:
        return templates.TemplateResponse(
            'errors/404.html',
            {
                'request': request
            }
        )
    elif status_code == 500:
        return templates.TemplateResponse(
            'errors/500.html', {
                'request': request,
                'detail': detail
            }
        )
    elif status_code == 401:
        return templates.TemplateResponse(
            'errors/401.html', {
                'request': request,
                'detail': detail
            }
        )
    else:
        # Generic error page
        return templates.TemplateResponse(
            'errors/default.html',
            {
                'request': request,
                'detail': detail
            }
        )
