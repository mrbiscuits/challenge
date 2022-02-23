import pytest
import json
import os
import sys
import unittest
from io import StringIO

from app.bootstrap import bootstrap

@pytest.fixture()
def flask_app():
    app = bootstrap()
    app.config['TESTING'] = True
    return app.test_client()

@pytest.mark.parametrize("value,cmd,expected", [(1, 'PUSH', [2,1]), (24, 'PUSH', [2, 24]), (490, 'PUSH', [2, 490]),  (2013, 'PUSH', [2, 2013])])
def test_push(flask_app, value, cmd, expected):
    response = flask_app.post('/api/fifth', json={'cmd': f'{cmd} {value}', 'stack': [2]})
    assert json.loads(response.data)["stack"] == expected
    assert response.status_code == 200

@pytest.mark.parametrize("value,cmd,expected", [(1, 'PUSH', [2,1]), (24, 'PUSH', [2, 24]), (490, 'PUSH', [2, 490]),  (2013, 'PUSH', [2, 2013])])
def test_push_shorthand(flask_app, value, cmd, expected):
    response = flask_app.post('/api/fifth', json={'cmd': f'{value}', 'stack': [2]})
    assert json.loads(response.data)["stack"] == expected
    assert response.status_code == 200

@pytest.mark.parametrize("stack,expected", [([3,2,2,2,2,2], [2,3,2,2,2,2])])
def test_swap(flask_app, stack, expected):
    response = flask_app.post('/api/fifth', json={'cmd': f'SWAP', 'stack': stack})
    json.loads(response.data)["stack"] == expected
    assert response.status_code == 200  

@pytest.mark.parametrize("stack", [[], [1]])
def test_invalid_swap(flask_app, stack):
    response = flask_app.post('/api/fifth', json={'cmd': f'SWAP', 'stack': stack})
    assert len(json.loads(response.data)["error"])
    assert response.status_code == 200  

@pytest.mark.parametrize("stack,expected", [([3,2], [2])])
def test_pop(flask_app, stack, expected):
    response = flask_app.post('/api/fifth', json={'cmd': f'POP', 'stack': stack})
    json.loads(response.data)["stack"] == expected
    assert response.status_code == 200  

def test_pop_empty(flask_app):
    response = flask_app.post('/api/fifth', json={'cmd': f'POP', 'stack': []})
    assert len(json.loads(response.data)["error"])
    assert response.status_code == 200  

@pytest.mark.parametrize("stack,expected", [([22], [22, 22]), ([2,2,3], [2,2,3,3])])
def test_dup(flask_app, stack, expected):
    response = flask_app.post('/api/fifth', json={'cmd': f'DUP', 'stack': stack})
    json.loads(response.data)["stack"] == expected
    assert response.status_code == 200  

def test_dup_empty(flask_app):
    response = flask_app.post('/api/fifth', json={'cmd': f'DUP', 'stack': []})
    assert len(json.loads(response.data)["error"])
    assert response.status_code == 200  

@pytest.mark.parametrize("stack", [[1], []])
def test_invalid_arithmatic(flask_app, stack):
    for operator in [op for op in '+-/*']:
        response = flask_app.post('/api/fifth', json={'cmd': f'{operator}', 'stack': stack})
    assert len(json.loads(response.data)["error"])
    assert response.status_code == 200  

@pytest.mark.parametrize("cmd", ['sda', '[]a', 'asdaaasd', '[1]', 'ASD 2'])
def test_invalid_cmd(flask_app, cmd):
    response = flask_app.post('/api/fifth', json={'cmd': f'{cmd}', 'stack': []})
    assert len(json.loads(response.data)["error"])
    assert response.status_code == 200  

@pytest.mark.parametrize("invalid_value", ["ab", "ABX", "TEN", "}", "1a1", None])
def test_push_invalid(flask_app, invalid_value):
    response = flask_app.post('/api/fifth', json={'cmd': f'PUSH {invalid_value}', 'stack': []})
    assert len(json.loads(response.data)["error"])
    assert response.status_code == 200  

@pytest.mark.parametrize("operator,stack,expected", [('+', [2,3], 5), ('-', [2,3], -1),('*', [2,3], 6),('/', [8,3], 3)])
def test_arithmatic(flask_app, operator, stack, expected):
    response = flask_app.post('/api/fifth', json={'cmd': f'{operator}', 'stack': stack})
    if operator == '+':
        assert json.loads(response.data)["stack"][0] == expected
    
    assert response.status_code == 200  

@pytest.mark.parametrize("value,cmd,expected", [(1, 'PUSH', [1,2]), (24, 'PUSH', [24,2]), (490, 'PUSH', [490, 2]),  (2013, 'PUSH', [2013,2])])
def test_push_rev(flask_app, value, cmd, expected):
    response = flask_app.post('/api/fifth', json={'cmd': f'{cmd} {value} REV', 'stack': [2]})
    assert json.loads(response.data)["stack"] == expected
    assert response.status_code == 200

@pytest.mark.parametrize("value,cmd,expected", [(1, 'PUSH', [1,2]), (24, 'PUSH', [24,2]), (490, 'PUSH', [490, 2]),  (2013, 'PUSH', [2013,2])])
def test_push_shorthand_rev(flask_app, value, cmd, expected):
    response = flask_app.post('/api/fifth', json={'cmd': f'{value} REV', 'stack': [2]})
    assert json.loads(response.data)["stack"] == expected
    assert response.status_code == 200

@pytest.mark.parametrize("stack,expected", [([3,2,2,2,2,2], [2,3,2,2,2,2])])
def test_swap_rev(flask_app, stack, expected):
    response = flask_app.post('/api/fifth', json={'cmd': f'SWAP  REV', 'stack': stack})
    json.loads(response.data)["stack"] == expected
    assert response.status_code == 200  
    
@pytest.mark.parametrize("stack,expected", [([22], [22, 22]), ([3,2,2], [3,3,2,2])])
def test_dup_rev(flask_app, stack, expected):
    response = flask_app.post('/api/fifth', json={'cmd': f'DUP REV', 'stack': stack})
    json.loads(response.data)["stack"] == expected
    assert response.status_code == 200  

