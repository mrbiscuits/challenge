from flask import Blueprint
challenge = Blueprint("challenge", __name__)

challenge.config = {}
@challenge.record
def record_params(setup_state):
    app = setup_state.app
    # challenge.config = dict([(key,value) for (key,value) in app.settings.items()])
    from app.challenge import urls  # noqa

