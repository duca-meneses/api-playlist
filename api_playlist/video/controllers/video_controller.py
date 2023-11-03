"""Creating VideoModel routers in api/v1/videos"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api_playlist.shared.database import get_session
from api_playlist.shared.exceptions import NotFound
from api_playlist.video.models.schemas import (
    VideoListModel,
    VideoRequestModel,
    VideoResponseModel,
)
from api_playlist.video.models.video_model import Video

router = APIRouter(prefix='/api/v1/videos')


@router.get('', response_model=VideoListModel, status_code=200)
def list_videos(
    db: Session = Depends(get_session),
) -> VideoListModel:
    videos = db.query(Video).all()
    return {'videos': videos}


@router.get('/{video_id}', response_model=VideoResponseModel, status_code=200)
def get_video(
    video_id: int, db: Session = Depends(get_session)
) -> VideoResponseModel:
    return search_video_by_id(video_id, db)


@router.post('', response_model=VideoResponseModel, status_code=201)
def create_video(
    video_request: VideoRequestModel, db: Session = Depends(get_session)
) -> VideoResponseModel:

    video = Video(**video_request.model_dump())

    db.add(video)
    db.commit()
    db.refresh(video)
    return video


@router.put('/{video_id}', response_model=VideoResponseModel, status_code=200)
def update_video(
    video_id: int,
    video_request: VideoRequestModel,
    db: Session = Depends(get_session),
) -> VideoResponseModel:
    video = search_video_by_id(video_id, db)
    video.title = video_request.title
    video.description = video_request.description
    video.url = video_request.url

    db.add(video)
    db.commit()
    db.refresh(video)
    return video


@router.delete('/{video_id}', status_code=204)
def delete_video(video_id: int, db: Session = Depends(get_session)) -> None:
    video = search_video_by_id(video_id, db)
    db.delete(video)
    db.commit()


def search_video_by_id(
    video_id: int, db: Session = Depends(get_session)
) -> VideoResponseModel:
    video = db.query(Video).get(video_id)

    if video is None:
        raise NotFound('Video')

    return video
