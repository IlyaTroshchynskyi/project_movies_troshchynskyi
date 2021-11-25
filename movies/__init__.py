# -*- coding: utf-8 -*-
"""
   Get access to the application with the config
"""

import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api
from flask_login import LoginManager, AnonymousUserMixin
from .config import init_logger


class MyAnonymousUser(AnonymousUserMixin):
    """
    Override Anonymous User from flask login to add new attributes
    """
    def __init__(self):
        self.email = ""

    def __repr__(self):
        return "Anonymous user"


db = SQLAlchemy()
migrate = Migrate()
api = Api(version="1.0", title="Films API", description="A simple Films API",)
login_manager = LoginManager()

login_manager.anonymous_user = MyAnonymousUser


def create_app(configuration):
    """
    Create and configure an instance of the Flask application.
    """

    init_logger("movies")
    app = Flask(__name__)
    app.config.from_object(configuration)

    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)

    login_manager.init_app(app)
    logger = logging.getLogger("movies.__init__")

    from . import models
    from .movies_app import users, directors, genres, films

    logger.info("Application movies has created")
    return app
