# -*- coding: utf-8 -*-
"""
   Collect all tests for project
"""

import http
import json
import pytest
from flask_login import current_user
from .data import genre_1, director_1, film_1, user_1, user_2, user_errors, user_fail


def test_get_users(client, auth):
    """
    Check http code
    """
    auth.registration()
    auth.login()
    resp = client.get("/registration")
    assert resp.status_code == http.HTTPStatus.OK, "HTTP code not equal 200"


def test_get_users_not_admin(client):
    """
    Check http code and response message after attempt get all users when user is not admin
    """
    client.post("/registration", data=json.dumps(user_2), content_type="application/json")
    client.post("/login", data=json.dumps({"email": user_2.get("email"),
                                           "password": user_2.get("password")}),
                content_type="application/json")
    resp = client.get("/registration")
    assert resp.status_code == http.HTTPStatus.FORBIDDEN, "HTTP code not equal 403"
    assert resp.json.get("message") == f"User with email: {user_2.get('email')} is not admin",\
        "Error messages are not correct"


def test_post_create_user(client):
    """
    Check http code and value of fields the object after adding to the db
    """
    resp = client.post("/registration", data=json.dumps(user_1), content_type="application/json")
    assert resp.status_code == http.HTTPStatus.CREATED, "HTTP code not equal 201"
    assert resp.json.get("first_name") == user_1.get("first_name"), "User name not equal"
    assert resp.json.get("last_name") == user_1.get("last_name"), "Last name of user not equal"
    assert resp.json.get("age") == user_1.get("age"), "Age of user not equal"
    assert resp.json.get("email") == user_1.get("email"), "Email of user not equal"
    assert resp.json.get("is_admin") is True, "Is admin not equal"


def test_post_create_user_invalid_data(client):
    """
    Check http code and the response message after attempt to update object by invalid data
    """
    resp = client.post("/registration", data=json.dumps(user_fail), content_type="application/json")
    assert resp.status_code == http.HTTPStatus.BAD_REQUEST, "HTTP code not equal 400"
    assert resp.json.get("message").get("errors") == user_errors,\
        "Error messages are not correct"


def test_post_create_user_exist_email(client):
    """
    Check http code and the response message after attempt to create user with existed email
    """
    client.post("/registration", data=json.dumps(user_1), content_type="application/json")
    resp = client.post("/registration", data=json.dumps(user_1), content_type="application/json")
    assert resp.status_code == http.HTTPStatus.CONFLICT, "HTTP code not equal 409"
    assert resp.json.get("message") == f"User with email: {user_1.get('email')} exist", \
        "Error messages are not correct"


def test_put_update_user(client):
    """
    Check http code and the value of fields the object after updating this object
    """
    client.post("/registration", data=json.dumps(user_1), content_type="application/json")
    client.post("/login", data=json.dumps({"email": user_1.get("email"),
                                           "password": user_1.get("password")}),
                content_type="application/json")
    resp = client.put("/registration/test2@mail.ru", data=json.dumps(user_2),
                      content_type="application/json")
    assert resp.status_code == http.HTTPStatus.OK, "HTTP code not equal 200"
    assert resp.json.get("first_name") == user_2.get("first_name"), "User name not equal"
    assert resp.json.get("last_name") == user_2.get("last_name"), "Last name of user not equal"
    assert resp.json.get("age") == user_2.get("age"), "Age of user not equal"
    assert resp.json.get("email") == user_2.get("email"), "Email of user not equal"
    assert resp.json.get("is_admin") is False, "Is admin not equal"


def test_put_update_user_not_admin(client):
    """
    Check http code and response message after attempt update user when you are not
    current user or not are admin
    """
    client.post("/registration", data=json.dumps(user_2), content_type="application/json")
    client.post("/registration", data=json.dumps(user_1), content_type="application/json")
    client.post("/login", data=json.dumps({"email": user_2.get("email"),
                                           "password": user_2.get("password")}),
                content_type="application/json")
    resp = client.put("/registration/test@mail.ru", data=json.dumps(user_2),
                      content_type="application/json")
    assert resp.status_code == http.HTTPStatus.FORBIDDEN, "HTTP code not equal 403"
    assert resp.json.get("message") == f"User with email: {current_user.email} is not admin " \
                                       f"or not current user",\
        "Error messages are not correct"


def test_put_user_invalid_data(client):
    """
    Check http code and the response message after attempt to update object by invalid data
    """
    client.post("/registration", data=json.dumps(user_1), content_type="application/json")
    client.post("/login", data=json.dumps({"email": user_1.get("email"),
                                           "password": user_1.get("password")}),
                content_type="application/json")
    resp = client.put("/registration/test2@mail.ru", data=json.dumps(user_fail),
                      content_type="application/json")
    assert resp.status_code == http.HTTPStatus.BAD_REQUEST, "HTTP code not equal 400"
    assert resp.json.get("message").get("errors") == user_errors,\
        "Error message are not correct"


def test_delete_user_by_email(client, auth):
    """
    Check http code after attempt to delete the user and that db is empty
    """
    auth.registration()
    auth.login()
    client.post("/registration", data=json.dumps(user_2), content_type="application/json")
    resp = client.delete("/registration/test3@mail.ru")
    assert resp.status_code == http.HTTPStatus.NO_CONTENT, "HTTP code not equal 204"
    assert len(client.get("/registration").json) == 1, "User not deleted"


def test_delete_user_by_email_not_admin(client):
    """
    Check http code after attempt to delete the user when user is not admin
    """
    client.post("/registration", data=json.dumps(user_2), content_type="application/json")
    client.post("/login", data=json.dumps({"email": user_2.get("email"),
                                           "password": user_2.get("password")}),
                content_type="application/json")
    resp = client.delete("/registration/test2@mail.ru")
    assert resp.status_code == http.HTTPStatus.FORBIDDEN, "HTTP code not equal 403"
    assert resp.json.get("message") == f"User with email: {current_user.email} is not admin", \
        "Error messages are not correct"


def test_delete_user_by_email_not_found(client, auth):
    """
    Check http code after attempt to delete non-existent user
    """
    auth.registration()
    auth.login()
    resp = client.delete("/registration/test3@mail.ru")
    assert resp.status_code == http.HTTPStatus.NOT_FOUND, "HTTP code not equal 404"


def test_post_login_user(auth):
    """
    Check http code and value of email after attempt to authorization
    """
    auth.registration()
    resp = auth.login()
    assert current_user.email == user_1.get("email", ""), "User unauthorized"
    assert resp.status_code == http.HTTPStatus.OK, "HTTP code not equal 200"


def test_post_logout_user(auth):
    """
    Check http code and value of email after attempt to logout
    """
    auth.registration()
    auth.login()
    resp = auth.logout()
    assert current_user.email == "", "User hasn't been logout"
    assert resp.status_code == http.HTTPStatus.OK, "HTTP code not equal 200"


@pytest.mark.parametrize("url, obj", [("/genres", genre_1),
                                      ("/directors", director_1), ("/films", film_1)])
def test_post_login_required(client, url, obj):
    """
    Check status code for routes where login required and user unauthorized
    """
    resp = client.post(url, data=json.dumps(obj), content_type="application/json")
    assert resp.status_code == http.HTTPStatus.UNAUTHORIZED, "User unauthorized"


@pytest.mark.parametrize("url, obj", [("/genres/1", genre_1),
                                      ("/directors/1", director_1), ("/films/1", film_1)])
def test_put_login_required(client, url, obj):
    """
    Check status code for routes where login required and user unauthorized
    """
    resp = client.put(url, data=json.dumps(obj), content_type="application/json")
    assert resp.status_code == http.HTTPStatus.UNAUTHORIZED, "User unauthorized"


@pytest.mark.parametrize("url,",  ["/genres/1", "/directors/1", "/films/1" ])
def test_delete_login_required(client, url):
    """
    Check status code for routes where login required and user unauthorized
    """
    resp = client.delete(url)
    assert resp.status_code == http.HTTPStatus.UNAUTHORIZED, "User unauthorized"
