import uvicorn
from fastapi import FastAPI

from api_playlist.shared.exceptions import NotFound
from api_playlist.shared.exceptions_handler import not_found_exceptions_handler
from api_playlist.video.controllers import video_controller

app = FastAPI()

app.include_router(video_controller.router)
app.add_exception_handler(NotFound, not_found_exceptions_handler)
