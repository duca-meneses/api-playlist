from fastapi import Request
from fastapi.responses import JSONResponse

from api_playlist.shared.exceptions import NotFound


def not_found_exceptions_handler(request: Request, exc: NotFound):
    return JSONResponse(
        status_code=404, content={'message': f'Oops! {exc.name} not found'}
    )
