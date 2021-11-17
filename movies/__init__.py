import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api
from flask_login import LoginManager
from .config import Configuration, init_logger


class MyAnonymousUser:

    @staticmethod
    def is_authenticated(self):
        return False

    def __repr__(self):
        return f'Anonymous user'


app = Flask(__name__)
app.config.from_object(Configuration)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app, version='1.0', title='Films API', description='A simple Films API',)
login_manager = LoginManager()

login_manager.anonymous_user = MyAnonymousUser
login_manager.init_app(app)
init_logger('movies')
logger = logging.getLogger("movies.__init__")

from . import models
from . import routes
from . import users
