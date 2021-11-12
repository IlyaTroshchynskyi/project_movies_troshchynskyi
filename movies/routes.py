from flask_restx import Resource
from flask_login import login_required, current_user
from . import api, db
from .models import Genres, Directors, Films
from flask import request
from .schemas import GenresSchemaLoad, GenresSchema, DirectorsSchemaLoad, DirectorsSchema, \
    FilmsSchema, FilmsSchemaLoad
from .utils import parse_films_json_data

genres_schema_load = GenresSchemaLoad()
genres_schema = GenresSchema()
directors_schema_load = DirectorsSchemaLoad()
directors_schema = DirectorsSchema()
films_schema = FilmsSchema()
films_schema_load = FilmsSchemaLoad()


@api.route('/genres')
class GenresListApi(Resource):
    def get(self):
        genres = Genres.query.all()
        return genres_schema.dump(genres, many=True)

    @login_required
    def post(self):
        genre = genres_schema_load.load(request.json, session=db.session)
        db.session.add(genre)
        db.session.commit()
        return genres_schema.dump(genre)


@api.route('/genres/<genre_id>')
class GenresListApi(Resource):
    def get(self, genre_id):
        genre = Genres.query.filter_by(genre_id=genre_id).first()
        if genre is None:
            return {'message': "Genre not found"}, 404
        return genres_schema.dump(genre)

    @login_required
    def put(self, genre_id):
        genre = Genres.query.filter_by(genre_id=genre_id).first()
        if genre is None:
            return {'message': "Genre not found"}, 404
        genre = genres_schema_load.load(request.json, instance=genre, session=db.session)
        db.session.add(genre)
        db.session.commit()
        return genres_schema.dump(genre)

    @login_required
    def delete(self, genre_id):
        genre = Genres.query.filter_by(genre_id=genre_id).first()
        if genre is None:
            return {'message': "Genre not found"}, 404
        db.session.delete(genre)
        db.session.commit()
        return {}, 204


@api.route('/directors')
class DirectorsListApi(Resource):
    def get(self):
        directors = Directors.query.all()
        return directors_schema.dump(directors, many=True)

    @login_required
    def post(self):
        director = directors_schema_load.load(request.json, session=db.session)
        db.session.add(director)
        db.session.commit()
        return directors_schema.dump(director)


@api.route('/directors/<director_id>')
class GenresListApi(Resource):
    def get(self, director_id):
        director = Directors.query.filter_by(director_id=director_id).first()
        if director is None:
            return {'message': "Director not found"}, 404
        return directors_schema.dump(director)

    @login_required
    def put(self, director_id):
        director = Directors.query.filter_by(director_id=director_id).first()
        if director is None:
            return {'message': "Director not found"}, 404
        director = directors_schema_load.load(request.json, instance=director, session=db.session)
        db.session.add(director)
        db.session.commit()
        return directors_schema.dump(director)

    @login_required
    def delete(self, director_id):
        director = Directors.query.filter_by(director_id=director_id).first()
        if director is None:
            return {'message': "Director not found"}, 404
        db.session.delete(director)
        db.session.commit()
        return {}, 204


@api.route('/films')
class FilmsListApi(Resource):

    def get(self):
        films = Films.query.all()
        return films_schema.dump(films, many=True)

    @login_required
    def post(self):
        input_ = parse_films_json_data(request.json)
        film = films_schema_load.load(input_, session=db.session, transient=True)
        directors = Directors.query.filter(Directors.director_id.in_(request.json.get('directors'))).all()
        genres = Genres.query.filter(Genres.genre_id.in_(request.json.get('genres'))).all()
        film.directors = directors
        film.genres = genres
        film.users = current_user
        db.session.add(film)
        db.session.commit()
        return films_schema.dump(film)


@api.route('/films/<film_id>')
class GenresListApi(Resource):
    def get(self, film_id):
        film = Films.query.filter_by(film_id=film_id).first()
        if film is None:
            return {'message': "Film not found"}, 404
        return films_schema.dump(film)

    @login_required
    def put(self, film_id):
        film = Films.query.filter_by(film_id=film_id).first()
        if film is None:
            return {'message': "Film not found"}, 404
        film = films_schema_load.load(parse_films_json_data(request.json),
                                      instance=film, session=db.session)
        directors = Directors.query.filter(Directors.director_id.in_(request.json.get('directors'))).all()
        genres = Genres.query.filter(Genres.genre_id.in_(request.json.get('genres'))).all()
        film.directors = directors
        film.genres = genres
        db.session.add(film)
        db.session.commit()
        return films_schema.dump(film)

    @login_required
    def delete(self, film_id):
        film = Films.query.filter_by(film_id=film_id).first()
        if film is None:
            return {'message': "Film not found"}, 404
        db.session.delete(film)
        db.session.commit()
        return {}, 204