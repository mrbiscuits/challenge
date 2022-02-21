import os
import pytest

from app.bootstrap import bootstrap
# from app.database import db as _db

def pytest_configure(config):
    import sys
    sys._called_from_test = True

def pytest_unconfigure(config):
    import sys
    del sys._called_from_test

@pytest.fixture(scope='session')
def app(request):
    """Session-wide test `Flask` application."""
    settings_override = {
        'TESTING': True
    }
    app = bootstrap()
    ctx = app.test_request_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app

