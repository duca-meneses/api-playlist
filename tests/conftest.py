import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from api_playlist.main import app
from api_playlist.shared.database import get_session
from api_playlist.shared.model import Base
from api_playlist.video.models.video_model import Video


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///./tests/test.db',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(engine)
    yield Session()
    Base.metadata.drop_all(engine)


@pytest.fixture
def client(session):
    def override_get_session():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = override_get_session
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def video(session):
    video = Video(
        title='Trailer Homem de Ferro',
        description='O primeiro filme do MCU nas tela do cinemas estreladas por Robert Downey Jr',
        url='http://www.youtube.com/watch?v=trailer',
    )
    session.add(video)
    session.commit()
    session.refresh(video)

    return video
