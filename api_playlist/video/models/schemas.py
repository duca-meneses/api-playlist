from pydantic import BaseModel, Field


class VideoResponseModel(BaseModel):
    id: int
    title: str
    description: str
    url: str
    # model_config = ConfigDict(from_atributes=True)

    class Config:
        from_attributes = True


class VideoListModel(BaseModel):
    videos: list[VideoResponseModel]


class VideoRequestModel(BaseModel):
    title: str = Field(min_length=3, max_length=50)
    description: str = Field(min_length=5, max_length=255)
    url: str = Field(min_length=5, max_length=255)
