import pytest
import json

from app.bootstrap import bootstrap

@pytest.fixture()
def flask_app():
    app = bootstrap()
    app.config['TESTING'] = True
    return app.test_client()

def test_home(flask_app):
    response = flask_app.get('/')
    assert response.status_code == 200

def test_healthcheck_returns_200_when_healthy(flask_app):
    response = flask_app.get('/api/healthcheck')
    assert response.status_code == 200

