# -*- coding: utf-8 -*-
"""
   Collect all fixtures for tests
"""
import json
import tempfile
import pytest

import movies
from movies import create_app, db
from movies.config import TestConfiguration
from movies.models import Genres


@pytest.fixture(scope='module')
def app():
    """
    Create and configure a new app instance for each test.
    """
    app = create_app(TestConfiguration)
    # db.create_all(app=app)

    print('app----------')
    yield app
    print('after yield up')
    # db.session.remove()
    # db.drop_all(app=app)


@pytest.fixture(scope="function", name='client')
def client(app):
    """
    A test client for the app.
    """
    db.create_all(app=app)
    yield app.test_client()
    db.session.remove()
    db.drop_all(app=app)

# @pytest.fixture(scope="function", name='login')
# def login(client):
#     user = {
#         "first_name": "Ilya",
#         "last_name": "Troshchynskyi",
#         "age": 27,
#         "email": "test2@mail.ru",
#         "password": "Test11111",
#         "is_admin": True
#     }
#     print('login')
#     client.post('/registration', data=json.dumps(user), content_type='application/json')
#     client.post('login', data=json.dumps({
#         "email": "test2@mail.ru",
#         "password": "Test11111"
#     }), content_type='application/json')


class AuthActions:
    def __init__(self, client):
        self._client = client

    def registration(self):

        user = {
                "first_name": "Ilya",
                "last_name": "Troshchynskyi",
                "age": 27,
                "email": "test2@mail.ru",
                "password": "Test11111",
                "is_admin": True
            }
        print('login')
        self._client.post('/registration', data=json.dumps(user), content_type='application/json')

    def login(self, email="test2@mail.ru", password="Test11111"):
        return self._client.post(
            "/login", data=json.dumps({"email": email, "password": password}), content_type='application/json'
        )

    def logout(self):
        return self._client.get("/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)