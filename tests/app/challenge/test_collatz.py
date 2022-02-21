import pytest
import json

from app.bootstrap import bootstrap

@pytest.fixture()
def flask_app():
    app = bootstrap()
    app.config['TESTING'] = True
    return app.test_client()

@pytest.mark.parametrize("input,expected", [(2, 1), (23, 15), (20, 7), (50, 24), (500001,112)])
def test_collatz(flask_app, input, expected):
    response = flask_app.post('/api/collatz', json={'cmd': f'COLLATZ {input}', 'stack': []})
    assert json.loads(response.data)["stack"][0] == expected
    assert response.status_code == 200

def test_must_be_positive_integer(flask_app):
    response = flask_app.post('/api/collatz', json={'cmd': 'COLLATZ 0', 'stack': []})
    assert response.status_code == 200
