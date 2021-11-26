# -*- coding: utf-8 -*-
"""
   Collect all tests for project
"""

import http
import json
from .data import genre_1, genre_2, genre_fail


def test_get_genres(client):
    """
    Check http code
    """
    resp = client.get("/genres")
    assert resp.status_code == http.HTTPStatus.OK, "HTTP code not equal 200"


def test_post_genres(client, auth):
    """
    Check http code and value of fields the object after adding to the db
    """
    auth.registration()
    auth.login()
    resp = client.post("/genres", data=json.dumps(genre_1), content_type="application/json")
    assert resp.status_code == http.HTTPStatus.CREATED, "HTTP code not equal 201"
    assert resp.json.get("genre_name") == genre_1.get("genre_name"), "Genre name not equal"


def test_post_genres_invalid_data(client, auth):
    """
    Check http code and the response message after attempt to add invalid data
    """
    auth.registration()
    auth.login()
    resp = client.post("/genres", data=json.dumps(genre_fail), content_type="application/json")
    assert resp.status_code == http.HTTPStatus.BAD_REQUEST, "HTTP code not equal 400"
    assert resp.json.get("message").get("errors") == \
           ["Length should be between 3 and 100 characters"], "Error message are not correct"


def test_get_genres_by_id(client, auth):
    """
    Check http code and value of fields the object after fetching by id
    """
    auth.registration()
    auth.login()
    client.post("/genres", data=json.dumps(genre_1), content_type="application/json")
    resp = client.get("/genres/1")
    assert resp.status_code == http.HTTPStatus.OK, "HTTP code not equal 200"
    assert resp.json.get("genre_name") == genre_1.get("genre_name"), "Genre name not equal"


def test_get_genres_by_not_found(client, auth):
    """
    Check http code after attempt to search non-existent genre
    """
    auth.registration()
    auth.login()
    client.post("/genres", data=json.dumps(genre_1), content_type="application/json")
    resp = client.get("/genres/2")
    assert resp.status_code == http.HTTPStatus.NOT_FOUND, "HTTP code not equal 404"


def test_put_genres(client, auth):
    """
    Check http code and the value of fields the object after updating this object
    """
    auth.registration()
    auth.login()
    client.post("/genres", data=json.dumps(genre_1), content_type="application/json")
    resp = client.put("/genres/1", data=json.dumps(genre_2), content_type="application/json")
    assert resp.status_code == http.HTTPStatus.OK, "HTTP code not equal 200"
    assert resp.json.get("genre_name") == genre_2.get("genre_name"), "Genre name not equal"


def test_put_genres_invalid_data(client, auth):
    """
    Check http code and the response message after attempt to update object by invalid data
    """
    auth.registration()
    auth.login()
    client.post("/genres", data=json.dumps(genre_1), content_type="application/json")
    resp = client.put("/genres/1", data=json.dumps(genre_fail), content_type="application/json")
    assert resp.status_code == http.HTTPStatus.BAD_REQUEST, "HTTP code not equal 400"
    assert resp.json.get("message").get("errors") == \
           ["Length should be between 3 and 100 characters"], "Error message are not correct"


def test_put_genres_not_found(client, auth):
    """
    Check http code after attempt to update non-existent genre
    """
    auth.registration()
    auth.login()
    resp = client.put("/genres/1", data=json.dumps(genre_1), content_type="application/json")
    assert resp.status_code == http.HTTPStatus.NOT_FOUND, "HTTP code not equal 404"


def test_delete_genre_by_id(client, auth):
    """
    Check http code after attempt to delete the genre and that db is empty
    """
    auth.registration()
    auth.login()
    client.post("/genres", data=json.dumps(genre_1), content_type="application/json")
    resp = client.delete("/genres/1")
    assert resp.status_code == http.HTTPStatus.NO_CONTENT, "HTTP code not equal 204"
    assert len(client.get("/genres").json) == 0, "Genre was not deleted"
