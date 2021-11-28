# -*- coding: utf-8 -*-
"""
   Collect all tests for project
"""

import pytest
from movies.schemas import ValidateSchemas
from .data import genre_1, director_1


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
