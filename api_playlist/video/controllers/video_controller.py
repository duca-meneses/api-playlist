from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from api_playlist.video.models.video_model import Video
from api_playlist.shared.dependencies import get_db

router = APIRouter(prefix="/api/v1/videos")

class VideoResponseModel(BaseModel):
    id: int
    title: str
    description: str
    url: str

    class Config:
        orm_mode = True


class VideoRequestModel(BaseModel):
    title: str = Field(min_length=3, max_length=50)
    description: str = Field(min_length=5, max_length=255)
    url: str = Field(min_length=5, max_length=255)


@router.get("", response_model=List[VideoResponseModel])
def list_videos(db: Session = Depends(get_db)) -> List[VideoResponseModel]:
    return db.query(Video).all()

@router.get("/{video_id}", response_model=VideoResponseModel)
def get_video(video_id: int, db: Session = Depends(get_db)) -> VideoResponseModel:
    return db.query(Video).get(video_id)


@router.post("", response_model=VideoResponseModel, status_code=201)
def create_video(video_request: VideoRequestModel, 
            db: Session = Depends(get_db)) -> VideoResponseModel:
    
    video = Video(
        **video_request.dict()
    )

    db.add(video)
    db.commit()
    db.refresh(video)

    return video

@router.put("/{video_id}", response_model=VideoResponseModel, status_code=200)
def update_video(video_id: int, video_request: VideoRequestModel, 
            db: Session = Depends(get_db)) -> VideoResponseModel:
    
    video = db.query(Video).get(video_id)
    video.title = video_request.title
    video.description = video_request.description
    video.url = video_request.url

    db.add(video)
    db.commit()
    db.refresh(video)
    
    return video

@router.delete("/{video_id}", status_code=204)
def delete_video(video_id: int, db: Session = Depends(get_db)) -> None:
    video = db.query(Video).get(video_id)
    db.delete(video)
    db.commit()