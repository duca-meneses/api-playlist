from fastapi.testclient import TestClient

from api_playlist.main import app
from api_playlist.shared.exceptions import NotFound
from api_playlist.shared.exceptions_handler import not_found_exceptions_handler
from api_playlist.video.controllers.video_controller import VideoResponseModel

client = TestClient(app)


def test_create_video(client):
    response = client.post(
        '/api/v1/videos',
        json={
            'title': 'Trailer Homem de ferro',
            'description': 'O primeiro filme do MCU',
            'url': 'http://www.youtube.com/watch?v=trailer',
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        'id': 1,
        'title': 'Trailer Homem de ferro',
        'description': 'O primeiro filme do MCU',
        'url': 'http://www.youtube.com/watch?v=trailer',
    }


def test_read_videos_with_empty_video(client):
    response = client.get('/api/v1/videos')
    assert response.status_code == 200
    assert response.json() == {'videos': []}


def test_read_videos_with_video(client, video):
    video_model = VideoResponseModel.model_validate(video).model_dump()
    response = client.get('/api/v1/videos')
    assert response.json() == {'videos': [video_model]}


def test_read_video_by_id(client, video):
    video_model = VideoResponseModel.model_validate(video).model_dump()
    response = client.get(f'/api/v1/videos/{video.id}')

    assert response.status_code == 200
    assert response.json() == video_model


def test_update_video(client, video):
    response = client.put(
        f'/api/v1/videos/{video.id}',
        json={
            'title': 'Title test',
            'description': 'Description test',
            'url': 'http://www.youtube.com/watch?v=test',
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        'id': 1,
        'title': 'Title test',
        'description': 'Description test',
        'url': 'http://www.youtube.com/watch?v=test',
    }


def test_delete_video(client, video):
    response = client.delete(f'/api/v1/videos/{video.id}')

    assert response.status_code == 204


def test_search_video_by_id(client, video):
    video_model = VideoResponseModel.model_validate(video).model_dump()
    response = client.get(f'/api/v1/videos/{video.id}')

    assert response.json() == video_model


# def test_search_video_by_id_not_found(client, video):

#     response = client.get(f"/videos/{video.id}1")

#     assert response.status_code == 404

#     assert response.json() == {"detail": 'Not Found'}
