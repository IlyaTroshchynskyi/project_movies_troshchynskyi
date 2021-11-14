from . import db
from .models import Genres, Directors


def parse_films_json(data):
    film_title = data.get('film_title')
    release_date = data.get('release_date')
    description = data.get('description')
    rate = data.get('rate')
    poster = data.get('poster')
    input_ = {"film_title": film_title, 'release_date': release_date, "description": description,
              "rate": rate, "poster": poster}
    return input_


def filter_by_genre(data):
    genres = []
    for gen in db.session.query().with_entities(Genres.genre_name).all():
        genres.append(gen[0])
    if isinstance(data.get('genre', genres), list):
        genre = genres
    else:
        genre = [data.get('genre')]
    return genre


def filter_by_directors(data):
    directors = []

    for director_last_name in db.session.query().with_entities(Directors.last_name).all():
        directors.append(director_last_name[0])
    if isinstance(data.get('director', directors), list):
        director = directors
    else:
        director = [data.get('director')]

    return director


def update_directors(data):
    directors = []
    for director in data.get('directors'):
        if Directors.query.filter_by(last_name=director.get('last_name', '')).first():
            directors.append(Directors.query.filter_by(last_name=director.get('last_name')).first())
    return directors


def update_genres(data):
    genres = []
    for genre in data.get('genres'):
        if Genres.query.filter_by(genre_name=genre.get('genre_name', '')).first():
            genres.append(Genres.query.filter_by(genre_name=genre.get('genre_name')).first())

    return genres