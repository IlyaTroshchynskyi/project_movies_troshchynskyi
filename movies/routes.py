from flask_restx import Resource
from . import api, db
from .models import Genres, Directors
from flask import request
from .schemas import GenresSchemaLoad, GenresSchema, DirectorsSchemaLoad, DirectorsSchema


genres_schema_load = GenresSchemaLoad()
genres_schema = GenresSchema()
directors_schema_load = DirectorsSchemaLoad()
directors_schema = DirectorsSchema()


@api.route('/genres')
class GenresListApi(Resource):
    def get(self):
        genres = Genres.query.all()
        return genres_schema.dump(genres, many=True)

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

    def put(self, genre_id):
        genre = Genres.query.filter_by(genre_id=genre_id).first()
        if genre is None:
            return {'message': "Genre not found"}, 404
        genre = genres_schema_load.load(request.json, instance=genre, session=db.session)
        db.session.add(genre)
        db.session.commit()
        return genres_schema.dump(genre)

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

    def put(self, director_id):
        director = Directors.query.filter_by(director_id=director_id).first()
        if director is None:
            return {'message': "Director not found"}, 404
        director = directors_schema_load.load(request.json, instance=director, session=db.session)
        db.session.add(director)
        db.session.commit()
        return directors_schema.dump(director)

    def delete(self, director_id):
        director = Directors.query.filter_by(director_id=director_id).first()
        if director is None:
            return {'message': "Director not found"}, 404
        db.session.delete(director)
        db.session.commit()
        return {}, 204