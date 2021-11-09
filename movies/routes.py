from flask_restx import Resource
from . import api, db
from .models import Genres
from flask import request
from .schemas import GenresSchemaLoad, GenresSchema


genres_schema_load = GenresSchemaLoad()
genres_schema = GenresSchema()


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