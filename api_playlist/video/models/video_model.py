from sqlalchemy import Column, Integer, String
 
from api_playlist.shared.database import Base


class Video(Base):
    __tablename__ = 'videos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50))
    description = Column(String(255))
    url = Column(String(255))