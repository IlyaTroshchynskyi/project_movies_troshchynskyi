# -*- coding: utf-8 -*-
"""
   Collect all fixtures for tests
"""
import json
import pytest
from movies import create_app, db
from movies.config import TestConfiguration
from .data import user_1


@pytest.fixture(scope='module')
def app():
    """
    Create and configure a new app instance for each test.
    """
    app = create_app(TestConfiguration)

    yield app


@pytest.fixture(scope="function", name='client')
def client(app):
    """
    A test client for the app.
    """
    db.create_all(app=app)
    with app.app_context():
        with app.test_client() as client:
            yield client
    db.session.remove()
    db.drop_all(app=app)


class AuthActions:
    """
    Class for authentication before tests
    """
    def __init__(self, client):
        self._client = client

    def registration(self):
        """
        Registration for user
        """
        self._client.post("/registration", data=json.dumps(user_1), content_type="application/json")

    def login(self, email="test2@mail.ru", password="Test11111"):
        """
        Login for user
        """
        return self._client.post(
            "/login", data=json.dumps({"email": email, "password": password}),
            content_type="application/json"
        )

    def logout(self):
        """
        Logout for user
        """
        return self._client.get("/logout")


@pytest.fixture
def auth(client):
    """
    Return class for authentication
    """
    return AuthActions(client)
