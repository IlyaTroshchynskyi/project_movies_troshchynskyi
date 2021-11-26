# -*- coding: utf-8 -*-
"""
   Collect all tests for project
"""

import http
import json
from .data import director_1, director_2, director_fail, director_errors


def test_get_directors(client):
    """
    Check http code
    """
    resp = client.get("/directors")
    assert resp.status_code == http.HTTPStatus.OK, "HTTP code not equal 200"


def test_post_directors(client, auth):
    """
    Check http code and value of fields the object after adding to the db
    """
    auth.registration()
    auth.login()
    resp = client.post("/directors", data=json.dumps(director_1), content_type="application/json")
    assert resp.status_code == http.HTTPStatus.CREATED, "HTTP code not equal 201"
    assert resp.json.get("first_name") == director_1.get("first_name"), \
        "First name of director not equal"
    assert resp.json.get("last_name") == director_1.get("last_name"), \
        "Last name of director not equal"
    assert resp.json.get("age") == director_1.get("age"), "Age of director not equal"


def test_post_director_invalid_data(client, auth):
    """
    Check http code and the response message after attempt to add invalid data
    """
    auth.registration()
    auth.login()
    resp = client.post("/directors", data=json.dumps(director_fail),
                       content_type="application/json")
    assert resp.status_code == http.HTTPStatus.BAD_REQUEST, "HTTP code not equal 400"
    assert resp.json.get("message").get("errors") == director_errors,\
        "Error messages are not correct"


def test_get_director_by_id(client, auth):
    """
    Check http code and value of fields the object after fetching by id
    """
    auth.registration()
    auth.login()
    client.post("/directors", data=json.dumps(director_1), content_type="application/json")
    resp = client.get("/directors/1")
    assert resp.status_code == http.HTTPStatus.OK, "HTTP code not equal 200"
    assert resp.json.get("first_name") == director_1.get("first_name"), \
        "First name of director not equal"
    assert resp.json.get("last_name") == director_1.get("last_name"), \
        "Last name of director not equal"
    assert resp.json.get("age") == director_1.get("age"), "Age of director not equal"


def test_get_directors_not_found(client):
    """
    Check http code after fetching non-existent director
    """
    resp = client.get("/directors/2")
    assert resp.status_code == http.HTTPStatus.NOT_FOUND, "HTTP code not equal 404"


def test_put_directors(client, auth):
    """
    Check http code and the value of fields the object after updating this object
    """
    auth.registration()
    auth.login()
    client.post("/directors", data=json.dumps(director_1), content_type="application/json")
    resp = client.put("/directors/1", data=json.dumps(director_2), content_type="application/json")
    assert resp.status_code == http.HTTPStatus.OK, "HTTP code not equal 200"
    assert resp.json.get("first_name") == director_2.get("first_name"),\
        "First name of director not updated"
    assert resp.json.get("last_name") == director_2.get("last_name"),\
        "Last name of director not updated"
    assert resp.json.get("age") == director_2.get("age"), "Age of director not updated"


def test_put_director_invalid_data(client, auth):
    """
    Check http code and the response message after attempt to update object by invalid data
    """
    auth.registration()
    auth.login()
    client.post("/directors", data=json.dumps(director_1), content_type="application/json")
    resp = client.put("/directors/1", data=json.dumps(director_fail),
                      content_type="application/json")
    assert resp.status_code == http.HTTPStatus.BAD_REQUEST, "HTTP code not equal 400"
    assert resp.json.get("message").get("errors") == director_errors,\
        "Error message are not correct"


def test_put_director_not_found(client, auth):
    """
    Check http code after attempt to update non-existent director
    """
    auth.registration()
    auth.login()
    resp = client.put("/directors/1", data=json.dumps(director_1), content_type="application/json")
    assert resp.status_code == http.HTTPStatus.NOT_FOUND, "HTTP code not equal 404"


def test_delete_director_by_id(client, auth):
    """
    Check http code after attempt to delete the director and that db is empty
    """
    auth.registration()
    auth.login()
    client.post("/directors", data=json.dumps(director_1), content_type="application/json")
    resp = client.delete("/directors/1")
    assert resp.status_code == http.HTTPStatus.NO_CONTENT, "HTTP code not equal 204"
    assert len(client.get("/directors").json) == 0, "Director not deleted"
