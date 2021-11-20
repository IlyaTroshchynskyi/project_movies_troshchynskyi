import http
import json
from flask import session

genre_1 = {"genre_name": "Боевик"}
genre_2 = {"genre_name": "Комедия"}
genre_fail = {"genre_name": ""}


director_1 = {"first_name": "Джон", "last_name": "Ландау", "age": 30}
director_2 = {"first_name": "Джон1", "last_name": "Ландау1", "age": 40}
director_fail = {"first_name": "", "last_name": "", "age": 0}

director_errors = ["Length first name should be between 3 and 100 characters",
                   "Length last name should be between 3 and 100 characters",
                   "The age should be more than 17"]


def test_get_genres(client):
    resp = client.get('/genres')
    assert resp.status_code == http.HTTPStatus.OK, 'HTTP code not equal 200'


def test_post_genres(client, auth):
    auth.registration()
    auth.login()
    resp = client.post('/genres', data=json.dumps(genre_1), content_type='application/json')
    assert resp.status_code == http.HTTPStatus.CREATED, 'HTTP code not equal 201'
    assert resp.json.get("genre_name") == "Боевик", 'Genre name not equal'


def test_post_genres_invalid_data(client, auth):
    auth.registration()
    auth.login()
    resp = client.post('/genres', data=json.dumps(genre_fail), content_type='application/json')
    assert resp.status_code == http.HTTPStatus.BAD_REQUEST, 'HTTP code not equal 400'
    assert resp.json.get("message").get('errors') == ["Length should be between 3 and 100 characters"],\
        'Error message are not correct'


def test_get_genres_by_id(client, auth):
    auth.registration()
    auth.login()
    client.post('/genres', data=json.dumps(genre_1), content_type='application/json')
    resp = client.get('/genres/1')
    assert resp.status_code == http.HTTPStatus.OK, 'HTTP code not equal 200'
    assert resp.json.get("genre_name") == "Боевик", 'Genre name not equal'


def test_get_genres_by_not_found(client, auth):
    auth.registration()
    auth.login()
    client.post('/genres', data=json.dumps(genre_1), content_type='application/json')
    resp = client.get('/genres/2')
    assert resp.status_code == http.HTTPStatus.NOT_FOUND, 'HTTP code not equal 404'


def test_put_genres(client, auth):
    auth.registration()
    auth.login()
    client.post('/genres', data=json.dumps(genre_1), content_type='application/json')
    resp = client.put('/genres/1', data=json.dumps(genre_2), content_type='application/json')
    assert resp.status_code == http.HTTPStatus.OK, 'HTTP code not equal 200'
    assert resp.json.get("genre_name") == "Комедия", 'Genre name not equal'


def test_put_genres_invalid_data(client, auth):
    auth.registration()
    auth.login()
    client.post('/genres', data=json.dumps(genre_1), content_type='application/json')
    resp = client.put('/genres/1', data=json.dumps(genre_fail), content_type='application/json')
    assert resp.status_code == http.HTTPStatus.BAD_REQUEST, 'HTTP code not equal 400'
    assert resp.json.get("message").get('errors') == ["Length should be between 3 and 100 characters"],\
        'Error message are not correct'


def test_put_genres_not_found(client, auth):
    auth.registration()
    auth.login()
    resp = client.put('/genres/1', data=json.dumps(genre_1), content_type='application/json')
    assert resp.status_code == http.HTTPStatus.NOT_FOUND, 'HTTP code not equal 404'


def test_delete_genre_by_id(client, auth):
    auth.registration()
    auth.login()
    client.post('/genres', data=json.dumps(genre_1), content_type='application/json')
    resp = client.delete('/genres/1')
    assert resp.status_code == http.HTTPStatus.NO_CONTENT, 'HTTP code not equal 204'
    assert len(client.get('/genres').json) == 0, 'Genre not deleted'


def test_post_genre_unauthorized(client):
    resp = client.post('/genres', data=json.dumps(genre_1), content_type='application/json')
    assert resp.status_code == http.HTTPStatus.UNAUTHORIZED, 'User unauthorized'


def test_put_genre_unauthorized(client):
    resp = client.put('/genres/1', data=json.dumps(genre_1), content_type='application/json')
    assert resp.status_code == http.HTTPStatus.UNAUTHORIZED, 'User unauthorized'


def test_delete_genre_unauthorized(client):
    resp = client.delete('/genres/1')
    assert resp.status_code == http.HTTPStatus.UNAUTHORIZED, 'User unauthorized'


def test_get_directors(client):
    resp = client.get('/directors')
    assert resp.status_code == http.HTTPStatus.OK, 'HTTP code not equal 200'


def test_post_directors(client, auth):
    auth.registration()
    auth.login()
    resp = client.post('/directors', data=json.dumps(director_1), content_type='application/json')
    assert resp.status_code == http.HTTPStatus.CREATED, 'HTTP code not equal 201'
    assert resp.json.get("first_name") == "Джон", 'First name of director not equal'
    assert resp.json.get("last_name") == "Ландау", 'Last name of director not equal'
    assert resp.json.get("age") == 30, 'Age of director not equal'


def test_post_director_invalid_data(client, auth):
    auth.registration()
    auth.login()
    resp = client.post('/directors', data=json.dumps(director_fail), content_type='application/json')
    assert resp.status_code == http.HTTPStatus.BAD_REQUEST, 'HTTP code not equal 400'
    assert resp.json.get("message").get('errors') == director_errors,\
        'Error messages are not correct'


def test_get_director_by_id(client, auth):
    auth.registration()
    auth.login()
    client.post('/directors', data=json.dumps(director_1), content_type='application/json')
    resp = client.get('/directors/1')
    assert resp.status_code == http.HTTPStatus.OK, 'HTTP code not equal 200'
    assert resp.json.get("first_name") == "Джон", 'First name of director not equal'
    assert resp.json.get("last_name") == "Ландау", 'Last name of director not equal'
    assert resp.json.get("age") == 30, 'Age of director not equal'


def test_get_directors_not_found(client, auth):
    resp = client.get('/directors/2')
    assert resp.status_code == http.HTTPStatus.NOT_FOUND, 'HTTP code not equal 404'


def test_put_directors(client, auth):
    auth.registration()
    auth.login()
    client.post('/directors', data=json.dumps(director_1), content_type='application/json')
    resp = client.put('/directors/1', data=json.dumps(director_2), content_type='application/json')
    assert resp.status_code == http.HTTPStatus.OK, 'HTTP code not equal 200'
    assert resp.json.get("first_name") == "Джон1", 'First name of director not updated'
    assert resp.json.get("last_name") == "Ландау1", 'Last name of director not updated'
    assert resp.json.get("age") == 40, 'Age of director not updated'


def test_put_director_invalid_data(client, auth):
    auth.registration()
    auth.login()
    client.post('/directors', data=json.dumps(director_1), content_type='application/json')
    resp = client.put('/directors/1', data=json.dumps(director_fail), content_type='application/json')
    assert resp.status_code == http.HTTPStatus.BAD_REQUEST, 'HTTP code not equal 400'
    assert resp.json.get("message").get('errors') == director_errors,\
        'Error message are not correct'


def test_put_director_not_found(client, auth):
    auth.registration()
    auth.login()
    resp = client.put('/directors/1', data=json.dumps(director_1), content_type='application/json')
    assert resp.status_code == http.HTTPStatus.NOT_FOUND, 'HTTP code not equal 404'


def test_delete_director_by_id(client, auth):
    auth.registration()
    auth.login()
    client.post('/directors', data=json.dumps(director_1), content_type='application/json')
    resp = client.delete('/directors/1')
    assert resp.status_code == http.HTTPStatus.NO_CONTENT, 'HTTP code not equal 204'
    assert len(client.get('/directors').json) == 0, 'Director not deleted'


def test_post_director_unauthorized(client):
    resp = client.post('/directors', data=json.dumps(director_1), content_type='application/json')
    assert resp.status_code == http.HTTPStatus.UNAUTHORIZED, 'User unauthorized'


def test_put_director_unauthorized(client):
    resp = client.put('/directors/1', data=json.dumps(director_1), content_type='application/json')
    assert resp.status_code == http.HTTPStatus.UNAUTHORIZED, 'User unauthorized'


def test_delete_director_unauthorized(client):
    resp = client.delete('/directors/1')
    assert resp.status_code == http.HTTPStatus.UNAUTHORIZED, 'User unauthorized'
