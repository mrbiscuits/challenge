from flask import Blueprint
operations = Blueprint("operations", __name__)

operations.config = {}
@operations.record
def record_params(setup_state):
    app = setup_state.app
    # operations.config = dict([(key,value) for (key,value) in app.settings.items()])
    from app.operations import urls  # noqa

