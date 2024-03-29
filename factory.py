"""
Factory that creates the APP object
"""

from flask import Flask
from conf.database import Config
from conf.base import Session
from flask_sqlalchemy_session import flask_scoped_session

"""
BLUEPRINT IMPORTS :
"""
from api.rest.onboarding import AUTHENTICATION_BLUEPRINT
from api.rest.notes import NOTES_BLUEPRINT


def create_app():
    """
    Construct the main application enclosing all Blueprints
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    flask_scoped_session(Session, app)
    app.register_blueprint(AUTHENTICATION_BLUEPRINT)
    app.register_blueprint(NOTES_BLUEPRINT)

    return app
