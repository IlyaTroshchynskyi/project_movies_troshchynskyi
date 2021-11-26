# -*- coding: utf-8 -*-
"""
   Collect all tests for project
"""


import json
from movies.models import Genres, Directors
from movies.movies_app.utils import parse_films_json, filter_by_genre, filter_by_directors, \
    update_directors, update_genres
from .data import genre_1, genre_2, director_1, director_2, film_1


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
