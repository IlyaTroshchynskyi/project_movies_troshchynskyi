# -*- coding: utf-8 -*-
"""
   Collect all tests for project
"""

import http
import json
import pytest
from flask_login import current_user
from movies.models import Genres, Directors
from movies.schemas import ValidateSchemas
from movies.utils import parse_films_json, filter_by_genre, filter_by_directors, \
    update_directors, update_genres
from .data import genre_1, genre_2, genre_fail, director_1, director_2, director_fail, \
    director_errors, film_1, film_2, film_3, film_4, film_5, film_fail, film_errors, \
    user_1, user_2, user_errors, user_fail


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


def test_parse_films_json():
    """
    Check that func return all fields except directors and genres
    """
    film = film_1.copy()
    film.pop("directors", "")
    film.pop("genres", "")
    assert film == parse_films_json(film_1), "Request data was parsed wrong"


def test_filter_by_genre(client, auth):
    """
    Check that func return list all genres when genres weren't found in db or
    return list genres which were defined in request params
    """
    auth.registration()
    auth.login()
    client.post("/genres", data=json.dumps(genre_1), content_type="application/json")
    client.post("/genres", data=json.dumps(genre_2), content_type="application/json")
    assert filter_by_genre({"test": "test"}) == ["Боевик", "Комедия"], "Filter by genre not equal"
    assert filter_by_genre({"genre": "Боевик"}) == ["Боевик"], "Filter by genre not equal"


def test_filter_by_director(client, auth):
    """
    Check that func return list all directors when genres weren't found in db or
    return list directors which were defined in request params
    """
    auth.registration()
    auth.login()
    client.post("/directors", data=json.dumps(director_1), content_type="application/json")
    client.post("/directors", data=json.dumps(director_2), content_type="application/json")
    assert filter_by_directors({"test": "test"}) == ["Ландау", "Ландау_Update"], \
        "Filter by director not equal"
    assert filter_by_directors({"director": "Ландау"}) == ["Ландау"], "Filter by director not equal"


def test_update_genres(client, auth):
    """
    Check that func return list genres by genre name
    """
    auth.registration()
    auth.login()
    client.post("/genres", data=json.dumps(genre_1), content_type="application/json")
    client.post("/genres", data=json.dumps(genre_2), content_type="application/json")
    client.post("/films", data=json.dumps(film_1), content_type="application/json")
    assert update_genres(film_1) == [Genres.query.filter_by(genre_id=1).first()], \
        "List Genres not equal for update"


def test_update_directors(client, auth):
    """
    Check that func return list directors by last name
    """
    auth.registration()
    auth.login()
    client.post("/directors", data=json.dumps(director_1), content_type="application/json")
    client.post("/films", data=json.dumps(film_1), content_type="application/json")
    assert update_directors(film_1) == [Directors.query.filter_by(director_id=1).first()], \
        "List Directors not equal for update"


@pytest.mark.parametrize("genre_name", ["F" * 101, "ff", "f", ""])
def test_validate_genre_name_length(genre_name):
    """
    Validate genre name length
    """
    assert ValidateSchemas.validate_genre({"genre_name": genre_name}) == \
           ["Length should be between 3 and 100 characters"], "Error message not equal"


@pytest.mark.parametrize("genre_name", ["323", "Fg44", 1111])
def test_validate_genre_name_string(genre_name):
    """
    Check that genre name should contains numbers
    """
    assert ValidateSchemas.validate_genre({"genre_name": genre_name}) == \
           ["The genre should be string"], "Error message not equal"


@pytest.mark.parametrize("first_name", ["F" * 101, "ff", "f", ""])
def test_validate_director_first_name_length(first_name):
    """
    Validate length of first name director
    """
    assert ValidateSchemas.validate_director({"first_name": first_name,
                                              "last_name": "Test",
                                              "age": 40}) == \
           ["Length first name should be between 3 and 100 characters"], \
        "Error message not equal"


@pytest.mark.parametrize("first_name", ["323", "Fg44", 1111])
def test_validate_director_first_name_string(first_name):
    """
    Check that first name of director don't contains numbers
    """
    assert ValidateSchemas.validate_director({"first_name": first_name,
                                              "last_name": "Test",
                                              "age": 40}) == ["The first name should be string"], \
        "Error message not equal"


@pytest.mark.parametrize("last_name", ["F" * 101, "ff", "f", ""])
def test_validate_director_last_name_length(last_name):
    """
    Validate length of last name director
    """
    assert ValidateSchemas.validate_director({"first_name": "Test",
                                              "last_name": last_name,
                                              "age": 40}) == \
           ["Length last name should be between 3 and 100 characters"], \
        "Error message not equal"


@pytest.mark.parametrize("last_name", ["323", "Fg44", 1111])
def test_validate_director_last_name_string(last_name):
    """
    Check that last name of director don't contains numbers
    """
    assert ValidateSchemas.validate_director({"first_name": "Test",
                                              "last_name": last_name,
                                              "age": 40}) == ["The last name should be string"], \
        "Error message not equal"


@pytest.mark.parametrize("age", ["323.f", "Fg44.", "17.5f"])
def test_validate_director_age_string(age):
    """
    Check that age of director don't contains letters
    """
    assert ValidateSchemas.validate_director({"first_name": "Test",
                                              "last_name": "Test",
                                              "age": age}) == ["Age should be numeric"], \
        "Error message not equal"


@pytest.mark.parametrize("age", [17, 0, 15])
def test_validate_director_age(age):
    """
    Check that age of director should be more than 17
    """
    assert ValidateSchemas.validate_director({"first_name": "Test",
                                              "last_name": "Test",
                                              "age": age}) == ["The age should be more than 17"], \
        "Error message not equal"


@pytest.mark.parametrize("age", [18.2, 55.1, 54.5])
def test_validate_director_age_numeric(age):
    """
    Check that age not float
    """
    assert ValidateSchemas.validate_director({"first_name": "Test",
                                              "last_name": "Test",
                                              "age": age}) ==\
           ["The age should be numeric not float"], "Error message not equal"


@pytest.mark.parametrize("first_name", ["F" * 101, "ff", "f", ""])
def test_validate_user_first_name_length(first_name):
    """
    Validate length of user's first name
    """
    assert ValidateSchemas.validate_user({"first_name": first_name,
                                          "last_name": "Test",
                                          "age": 40,
                                          "email": "test2@mail.ru",
                                          "password": "Test11111"}) == \
           ["Length first name should be between 3 and 100 characters"], \
        "Error message not equal"


@pytest.mark.parametrize("first_name", ["323", "Fg44", 1111])
def test_validate_user_first_name_string(first_name):
    """
    Check that first name of user don't contains numbers
    """
    assert ValidateSchemas.validate_user({"first_name": first_name,
                                          "last_name": "Test", "age": 40,
                                          "email": "test2@mail.ru",
                                          "password": "Test11111"}) == \
           ["The first name should be string"], "Error message not equal"


@pytest.mark.parametrize("last_name", ["F" * 101, "ff", "f", ""])
def test_validate_user_last_name_length(last_name):
    """
    Validate length of user's last name
    """
    assert ValidateSchemas.validate_director({"first_name": "Test",
                                              "last_name": last_name,
                                              "age": 40,
                                              "email": "test2@mail.ru",
                                              "password": "Test11111"}) == \
           ["Length last name should be between 3 and 100 characters"], "Error message not equal"


@pytest.mark.parametrize("last_name", ["323", "Fg44", 1111])
def test_validate_user_last_name_string(last_name):
    """
    Check that last name of user don't contains numbers
    """
    assert ValidateSchemas.validate_user({"first_name": "Test",
                                          "last_name": last_name,
                                          "age": 40,
                                          "email": "test2@mail.ru",
                                          "password": "Test11111"}) == \
           ["The last name should be string"], "Error message not equal"


@pytest.mark.parametrize("age", ["323.f", "Fg44.", "17.5f"])
def test_validate_user_age_string(age):
    """
    Check that age of director don't contains letters
    """
    assert ValidateSchemas.validate_user({"first_name": "Test",
                                          "last_name": "Test",
                                          "age": age,
                                          "email": "test2@mail.ru",
                                          "password": "Test11111"}) == ["Age should be numeric"], \
        "Error message not equal"


@pytest.mark.parametrize("age", [11, 0, 10])
def test_validate_user_age(age):
    """
    Check that age of user should be more than 11
    """
    assert ValidateSchemas.validate_user({"first_name": "Test",
                                          "last_name": "Test",
                                          "age": age,
                                          "email": "test2@mail.ru",
                                          "password": "Test11111"}) == \
           ["The age should be more than 11"], "Error message not equal"


@pytest.mark.parametrize("age", [12.2, 55.1, 54.5])
def test_validate_user_age_numeric(age):
    """
    Check that age not float
    """
    assert ValidateSchemas.validate_user({"first_name": "Test",
                                          "last_name": "Test",
                                          "age": age,
                                          "email": "test2@mail.ru",
                                          "password": "Test11111"}) == \
           ["The age should be numeric not float"], "Error message not equal"


@pytest.mark.parametrize("email", ["tes.mail.ru", "t@.ru", "t@.ru"])
def test_validate_user_email(email):
    """
    Validate user's email
    """
    assert ValidateSchemas.validate_user({"first_name": "Test",
                                          "last_name": "Test",
                                          "age": 18,
                                          "email": email,
                                          "password": "Test11111"}) == ["Invalid email"]


@pytest.mark.parametrize("password", ["ttsdsdsds33", "rere3", "Test"])
def test_validate_user_password(password):
    """
    Validate user's password
    """
    assert ValidateSchemas.validate_user({"first_name": "Test",
                                          "last_name": "Test",
                                          "age": 18,
                                          "email": "test2@mail.ru",
                                          "password": password}) == \
           ["Make sure your password is at lest 8 letters, has a number in it, "
            "has a capital letter in it"], "Error message not equal"


@pytest.mark.parametrize("film_title", ["F" * 101, "ff", "f", ""])
def test_validate_film_title_length(film_title):
    """
    Validate length of film title
    """
    assert ValidateSchemas.validate_films({"film_title": film_title,
                                           "release_date": "2009-07-23",
                                           "description": "Аватар",
                                           "rate": 9.0,
                                           "poster": "www.google.com",
                                           "directors": [director_1],
                                           "genres": [genre_1]}) == \
           ["Length film title should be between 3 and 100 characters"], "Error message not equal"


@pytest.mark.parametrize("film_title", ["2340", "3323", "42423"])
def test_validate_film_title_string(film_title):
    """
    Check that film title don't contains numbers
    """
    assert ValidateSchemas.validate_films({"film_title": film_title,
                                           "release_date": "2009-07-23",
                                           "description": "Аватар",
                                           "rate": 9.0,
                                           "poster": "www.google.com",
                                           "directors": [director_1],
                                           "genres": [genre_1]}) == \
           ["The film title should be string"], "Error message not equal"


@pytest.mark.parametrize("release_date", ["1970-01-01", "1970-12-31", "1970-12-30"])
def test_validate_film_release_date(release_date):
    """
    Check that release date of film more or equal 1971-01-01
    """
    assert ValidateSchemas.validate_films({"film_title": "Аватар",
                                           "release_date": release_date,
                                           "description": "Аватар",
                                           "rate": 9.0,
                                           "poster": "www.google.com",
                                           "directors": [director_1],
                                           "genres": [genre_1]}) == \
           ["Release data should be more than 1971-01-01"], "Error message not equal"


@pytest.mark.parametrize("rate", ["sd34", "4.2r", "10"])
def test_validate_film_rate(rate):
    """
    Check that rate float
    """
    assert ValidateSchemas.validate_films({"film_title": "Аватар",
                                           "release_date": "2009-07-23",
                                           "description": "Аватар",
                                           "rate": rate,
                                           "poster": "www.google.com",
                                           "directors": [director_1],
                                           "genres": [genre_1]}) == \
           ["The rate should be float"], "Error message not equal"


@pytest.mark.parametrize("rate", [-1.0, -0.1, -0.0001, 10.1, 11.0])
def test_validate_film_rate_borders(rate):
    """
    Check that rate between 0 and 10
    """
    assert ValidateSchemas.validate_films({"film_title": "Аватар",
                                           "release_date": "2009-07-23",
                                           "description": "Аватар",
                                           "rate": rate,
                                           "poster": "www.google.com",
                                           "directors": [director_1],
                                           "genres": [genre_1]}) == \
           ["Rate should be between 0 and 10"], "Error message not equal"


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
