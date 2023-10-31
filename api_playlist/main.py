import uvicorn
from fastapi import FastAPI

from api_playlist.video.controllers import video_controller

app = FastAPI()

app.include_router(video_controller.router)


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
