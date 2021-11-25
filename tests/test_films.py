# -*- coding: utf-8 -*-
"""
   Collect all tests for project
"""

import http
import json
from flask_login import current_user
from .data import genre_1, genre_2, director_1, director_2, film_1, film_2, film_3, film_4, \
    film_5, film_fail, film_errors, user_1, user_2


def test_get_films(client):
    """
    Check http code
    """
    resp = client.get("/films")
    assert resp.status_code == http.HTTPStatus.OK, "HTTP code not equal 200"


def test_post_films(client, auth):
    """
    Check http code and value of fields the object after adding to the db
    """
    auth.registration()
    auth.login()
    client.post("/genres", data=json.dumps(genre_1), content_type="application/json")
    client.post("/directors", data=json.dumps(director_1), content_type="application/json")
    resp = client.post("/films", data=json.dumps(film_1), content_type="application/json")
    assert resp.status_code == http.HTTPStatus.CREATED, "HTTP code not equal 201"
    assert resp.json.get("film_title") == film_1.get("film_title"), "Film title not equal"
    assert resp.json.get("release_date") == film_1.get("release_date"), \
        "Release Date of director not equal"
    assert resp.json.get("description") == film_1.get("description"), \
        "Description of film not equal"
    assert resp.json.get("rate") == film_1.get("rate"), "Rate of film not equal"
    assert resp.json.get("poster") == film_1.get("poster"), "Poster of film not equal"
    assert resp.json.get("directors")[0].get("first_name") == director_1.get("first_name"),\
        "Director's name of film not equal"
    assert resp.json.get("directors")[0].get("last_name") == director_1.get("last_name"),\
        "Director's last name of film not equal"
    assert resp.json.get("directors")[0].get("age") == director_1.get("age"),\
        "Director's age of film not equal"
    assert resp.json.get("genres")[0].get("genre_name") == genre_1.get("genre_name"),\
        "Genre of film not equal"


def test_post_film_invalid_data(client, auth):
    """
    Check http code and the response message after attempt to add invalid data
    """
    auth.registration()
    auth.login()
    resp = client.post("/films", data=json.dumps(film_fail), content_type="application/json")
    assert resp.status_code == http.HTTPStatus.BAD_REQUEST, "HTTP code not equal 400"
    assert resp.json.get("message").get("errors") == film_errors,\
        "Error messages are not correct"


def test_get_film_by_id(client, auth):
    """
    Check http code and value of fields the object after fetching by id
    """
    auth.registration()
    auth.login()
    client.post("/films", data=json.dumps(film_1), content_type="application/json")
    resp = client.get("/films/1")
    assert resp.status_code == http.HTTPStatus.OK, "HTTP code not equal 200"
    assert resp.json.get("film_title") == film_1.get("film_title"), "Film title not equal"
    assert resp.json.get("release_date") == film_1.get("release_date"), \
        "Release Date of director not equal"
    assert resp.json.get("description") == film_1.get("description"),\
        "Description of film not equal"
    assert resp.json.get("rate") == film_1.get("rate"), "Rate of film not equal"
    assert resp.json.get("poster") == film_1.get("poster"), "Poster of film not equal"


def test_get_films_by_search(client, auth):
    """
    Check http code and value of film title after filtering by partial or full coincidence title
    """
    auth.registration()
    auth.login()
    client.post("/genres", data=json.dumps(genre_1), content_type="application/json")
    client.post("/directors", data=json.dumps(director_1), content_type="application/json")
    client.post("/genres", data=json.dumps(genre_2), content_type="application/json")
    client.post("/directors", data=json.dumps(director_2), content_type="application/json")
    client.post("/films", data=json.dumps(film_1), content_type="application/json")
    client.post("/films", data=json.dumps(film_2), content_type="application/json")
    client.post("/films", data=json.dumps(film_3), content_type="application/json")
    resp = client.get("/films?search=Железный")
    assert resp.status_code == http.HTTPStatus.OK, "HTTP code not equal 200"
    assert resp.json[0].get("film_title") == "Железный человек 3", \
        "Film title not equal use search param"


def test_get_films_by_release_date(client, auth):
    """
    Check http code and value of film title after filtering by release_date
    """
    auth.registration()
    auth.login()
    client.post("/genres", data=json.dumps(genre_1), content_type="application/json")
    client.post("/directors", data=json.dumps(director_1), content_type="application/json")
    client.post("/genres", data=json.dumps(genre_2), content_type="application/json")
    client.post("/directors", data=json.dumps(director_2), content_type="application/json")
    client.post("/films", data=json.dumps(film_1), content_type="application/json")
    client.post("/films", data=json.dumps(film_2), content_type="application/json")
    client.post("/films", data=json.dumps(film_3), content_type="application/json")
    client.post("/films", data=json.dumps(film_4), content_type="application/json")
    client.post("/films", data=json.dumps(film_5), content_type="application/json")
    resp = client.get("/films?start_date=2019-06-24")
    assert resp.status_code == http.HTTPStatus.OK, "HTTP code not equal 200"
    assert resp.json[0].get("film_title") in ["Миньйоны", "Аладдин"],\
        "Film title not equal use release_date param"
    assert resp.json[1].get("film_title") in ["Миньйоны", "Аладдин"], \
        "Film title not equal use release_date param"


def test_get_films_by_rate(client, auth):
    """
    Check http code and value of film title after filtering by rate
    """
    auth.registration()
    auth.login()
    client.post("/genres", data=json.dumps(genre_1), content_type="application/json")
    client.post("/directors", data=json.dumps(director_1), content_type="application/json")
    client.post("/genres", data=json.dumps(genre_2), content_type="application/json")
    client.post("/directors", data=json.dumps(director_2), content_type="application/json")
    client.post("/films", data=json.dumps(film_1), content_type="application/json")
    client.post("/films", data=json.dumps(film_2), content_type="application/json")
    client.post("/films", data=json.dumps(film_3), content_type="application/json")
    client.post("/films", data=json.dumps(film_4), content_type="application/json")
    client.post("/films", data=json.dumps(film_5), content_type="application/json")
    resp = client.get("/films?rate=10")
    assert resp.status_code == http.HTTPStatus.OK, "HTTP code not equal 200"
    assert resp.json[0].get("film_title") == "Аватар1",\
        "Film title not equal use rate param"


def test_get_films_by_genre(client, auth):
    """
    Check http code and value of film title after filtering by genre name
    """
    auth.registration()
    auth.login()
    client.post("/genres", data=json.dumps(genre_1), content_type="application/json")
    client.post("/directors", data=json.dumps(director_1), content_type="application/json")
    client.post("/genres", data=json.dumps(genre_2), content_type="application/json")
    client.post("/directors", data=json.dumps(director_2), content_type="application/json")
    client.post("/films", data=json.dumps(film_1), content_type="application/json")
    client.post("/films", data=json.dumps(film_2), content_type="application/json")
    client.post("/films", data=json.dumps(film_3), content_type="application/json")
    client.post("/films", data=json.dumps(film_4), content_type="application/json")
    client.post("/films", data=json.dumps(film_5), content_type="application/json")
    resp = client.get("/films?genre=Боевик")
    assert resp.status_code == http.HTTPStatus.OK, "HTTP code not equal 200"
    assert resp.json[0].get("film_title") in ["Аватар", "Миньйоны"],\
        "Film title not equal use genre param"
    assert resp.json[1].get("film_title") in ["Аватар", "Миньйоны"],\
        "Film title not equal use genre param"
    assert len(resp.json) == 2, "Length of json not equal"


def test_get_films_by_director(client, auth):
    """
    Check http code and value of film title after filtering by director last name
    """
    auth.registration()
    auth.login()
    client.post("/genres", data=json.dumps(genre_1), content_type="application/json")
    client.post("/directors", data=json.dumps(director_1), content_type="application/json")
    client.post("/genres", data=json.dumps(genre_2), content_type="application/json")
    client.post("/directors", data=json.dumps(director_2), content_type="application/json")
    client.post("/films", data=json.dumps(film_1), content_type="application/json")
    client.post("/films", data=json.dumps(film_2), content_type="application/json")
    client.post("/films", data=json.dumps(film_3), content_type="application/json")
    client.post("/films", data=json.dumps(film_4), content_type="application/json")
    client.post("/films", data=json.dumps(film_5), content_type="application/json")
    resp = client.get("/films?director=Ландау")
    assert resp.status_code == http.HTTPStatus.OK, "HTTP code not equal 200"
    assert resp.json[0].get("film_title") in ["Аватар", "Миньйоны"],\
        "Film title not equal use genre param"
    assert resp.json[1].get("film_title") in ["Аватар", "Миньйоны"],\
        "Film title not equal use genre param"
    assert len(resp.json) == 2, "Length of json not equal"


def test_get_films_by_combine_filter(client, auth):
    """
    Check http code and value of film title after filtering by combined filter.
    Was used Params: "start_date", "end_date", "rate", "genre", "director"
    """
    auth.registration()
    auth.login()
    client.post("/genres", data=json.dumps(genre_1), content_type="application/json")
    client.post("/directors", data=json.dumps(director_1), content_type="application/json")
    client.post("/genres", data=json.dumps(genre_2), content_type="application/json")
    client.post("/directors", data=json.dumps(director_2), content_type="application/json")
    client.post("/films", data=json.dumps(film_1), content_type="application/json")
    client.post("/films", data=json.dumps(film_2), content_type="application/json")
    client.post("/films", data=json.dumps(film_3), content_type="application/json")
    client.post("/films", data=json.dumps(film_4), content_type="application/json")
    client.post("/films", data=json.dumps(film_5), content_type="application/json")
    resp = client.get\
        ("/films?rate=9.2&genre=Комедия&director=Ландау_Update&release_date=2019-07-24")
    assert resp.status_code == http.HTTPStatus.OK, "HTTP code not equal 200"
    assert resp.json[0].get("film_title") == "Аладдин", "Film title not equal use combine params"


def test_get_film_not_found(client):
    """
    Check http code after fetching non-existent director
    """
    resp = client.get("/films/2")
    assert resp.status_code == http.HTTPStatus.NOT_FOUND, "HTTP code not equal 404"


def test_put_film(client, auth):
    """
    Check http code and the value of fields the object after updating this object
    """
    auth.registration()
    auth.login()
    client.post("/genres", data=json.dumps(genre_1), content_type="application/json")
    client.post("/directors", data=json.dumps(director_1), content_type="application/json")
    client.post("/genres", data=json.dumps(genre_2), content_type="application/json")
    client.post("/directors", data=json.dumps(director_2), content_type="application/json")
    client.post("/films", data=json.dumps(film_1), content_type="application/json")
    resp = client.put("/films/1", data=json.dumps(film_2), content_type="application/json")
    assert resp.status_code == http.HTTPStatus.OK, "HTTP code not equal 200"
    assert resp.json.get("film_title") == film_2.get("film_title"), "Film title wasn't updated"
    assert resp.json.get("release_date") == film_2.get("release_date"), \
        "Release Date wasn't updated"
    assert resp.json.get("description") == film_2.get("description"),\
        "Description of film wasn't updated"
    assert resp.json.get("rate") == film_2.get("rate"), "Rate of film wasn't updated"
    assert resp.json.get("poster") == film_2.get("poster"), "Poster of film wasn't updated"
    assert resp.json.get("directors")[0].get("first_name") == director_2.get("first_name"), \
        "Director's name of film not equal"
    assert resp.json.get("directors")[0].get("last_name") == director_2.get("last_name"), \
        "Director's last name of film not equal"
    assert resp.json.get("directors")[0].get("age") == director_2.get("age"), \
        "Director's age of film not equal"
    assert resp.json.get("genres")[0].get("genre_name") == genre_2.get("genre_name"), \
        "Genre of film not equal"


def test_put_film_not_admin(client):
    """
    Check http code and the error message when user wants update film
    which was added by other user or current user is not admin.
    """
    client.post("/registration", data=json.dumps(user_1), content_type="application/json")
    client.post("/registration", data=json.dumps(user_2), content_type="application/json")
    client.post("/login", data=json.dumps({"email": user_1.get("email"),
                                           "password": user_1.get("password")}),
                content_type="application/json")
    client.post("/directors", data=json.dumps(director_1), content_type="application/json")
    client.post("/genres", data=json.dumps(genre_1), content_type="application/json")
    client.post("/films", data=json.dumps(film_1), content_type="application/json")
    client.get("/logout")
    client.post("/login", data=json.dumps({"email": user_2.get("email"),
                                           "password": user_2.get("password")}),
                content_type="application/json")
    resp = client.put("/films/1", data=json.dumps(film_2), content_type="application/json")
    assert resp.status_code == http.HTTPStatus.FORBIDDEN, "HTTP code not equal 403"
    assert resp.json.get("message") == f"User with email: {current_user.email} is not " \
                                       "admin or did not create this film", \
        "Error message are not correct"


def test_put_film_invalid_data(client, auth):
    """
    Check http code and the response message after attempt to update object by invalid data
    """
    auth.registration()
    auth.login()
    client.post("/films", data=json.dumps(film_1), content_type="application/json")
    resp = client.put("/films/1", data=json.dumps(film_fail), content_type="application/json")
    assert resp.status_code == http.HTTPStatus.BAD_REQUEST, "HTTP code not equal 400"
    assert resp.json.get("message").get("errors") == film_errors,\
        "Error message are not correct"


def test_put_film_not_found(client, auth):
    """
    Check http code after attempt to update non-existent film
    """
    auth.registration()
    auth.login()
    resp = client.put("/film/1", data=json.dumps(film_1), content_type="application/json")
    assert resp.status_code == http.HTTPStatus.NOT_FOUND, "HTTP code not equal 404"


def test_delete_film_by_id(client, auth):
    """
    Check http code after attempt to delete the film and that db is empty
    """
    auth.registration()
    auth.login()
    client.post("/films", data=json.dumps(film_1), content_type="application/json")
    resp = client.delete("/films/1")
    assert resp.status_code == http.HTTPStatus.NO_CONTENT, "HTTP code not equal 204"
    assert len(client.get("/films").json) == 0, "Director not deleted"


def test_delete_film_by_id_not_admin(client):
    """
    Check http code after attempt to delete the film when user is not admin or this
    film was created by other user
    """
    client.post("/registration", data=json.dumps(user_1), content_type="application/json")
    client.post("/registration", data=json.dumps(user_2), content_type="application/json")
    client.post("/login", data=json.dumps({"email": user_1.get("email"),
                                           "password": user_1.get("password")}),
                content_type="application/json")
    client.post("/directors", data=json.dumps(director_1), content_type="application/json")
    client.post("/genres", data=json.dumps(genre_1), content_type="application/json")
    client.post("/films", data=json.dumps(film_1), content_type="application/json")
    client.get("/logout")
    client.post("/login", data=json.dumps({"email": user_2.get("email"),
                                           "password": user_2.get("password")}),
                content_type="application/json")
    resp = client.delete("/films/1")
    assert resp.status_code == http.HTTPStatus.FORBIDDEN, "HTTP code not equal 403"
    assert resp.json.get("message") == f"User with email: {current_user.email} is not " \
                                       "admin or did not create this film", \
        "Error message are not correct"
