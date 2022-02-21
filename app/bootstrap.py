import os
import logging
import sys
import traceback

from flask import Flask, send_from_directory

def bootstrap():
    """
    Bootstrap function that loads the config and registers the Blueprint routes
    into the Flask app.
    """
    configure_prefork_logging()
    logging.debug('Challenge App spinning up!!')
    instance_path = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, "config"))
    app = Flask(__name__, instance_path=instance_path, instance_relative_config=True)
    
    from app.challenge import challenge as challenge_blueprint
    from app.operations import operations as operations_blueprint
    app.register_blueprint(challenge_blueprint)
    app.register_blueprint(operations_blueprint)
    configure_postfork_logging(app)
    return app

def configure_postfork_logging(app):
    """
    Postfork we set the root logger handler which was added prefork and then
    configure based on users application config
    """
    root = logging.getLogger("")
    root.removeHandler(root.handlers[0])

def configure_prefork_logging():
    """
    To ensure we have logging visibility before the app is initialised postfork
    we set the root logger to emit to stdout
    """
    logging.getLogger("").addHandler(logging.StreamHandler(sys.stdout))
    logging.getLogger("").setLevel(logging.INFO)
