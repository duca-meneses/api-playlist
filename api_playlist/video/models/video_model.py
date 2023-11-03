from sqlalchemy.orm import Mapped, mapped_column

from api_playlist.shared.model import Base


class Video(Base):
    __tablename__ = 'videos'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    url: Mapped[str]
