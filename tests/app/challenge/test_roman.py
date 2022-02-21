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

VALID_NUMERALS = [(1, 'I'), (3, 'III'), (4, 'IV'), (9, 'IX'), (14, 'XIV'),
            (19, 'XIX'), (24, 'XXIV'), (40, 'XL'), (49, 'XLIX'), (90, 'XC'),
            (99, 'XCIX'), (400, 'CD'), (490, 'CDXC'), (499, 'CDXCIX'),
            (990, 'CMXC'), (998, 'CMXCVIII'), (999, 'CMXCIX'),
            (2013, 'MMXIII')]

INVALID_NUMERALS = ['A', 'BIII', 'XIIIII','CXXXX', 'MCCCCXII']

@pytest.mark.parametrize("value,numeral", VALID_NUMERALS)
def test_individual_romans(flask_app, value, numeral):
    response = flask_app.post('/api/roman', json={'cmd': f'ROMAN {numeral}', 'stack': []})
    assert json.loads(response.data)["stack"][0] == value
    assert response.status_code == 200

@pytest.mark.parametrize("numeral", INVALID_NUMERALS)
def test_invalid_romans(flask_app, numeral):
    response = flask_app.post('/api/roman', json={'cmd': f'ROMAN {numeral}', 'stack': []})
    assert len(json.loads(response.data)["error"])
    assert response.status_code == 200
