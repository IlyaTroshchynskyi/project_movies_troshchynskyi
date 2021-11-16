from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1@localhost:5432/dbname'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app, version='1.0', title='Films API', description='A simple Films API',)
login_manager = LoginManager()
login_manager.init_app(app)

from . import models
from . import routes
from . import users
