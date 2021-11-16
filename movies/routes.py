from datetime import date
from flask import request, abort
from flask_restx import Resource, fields
from flask_login import login_required, current_user
from . import api, db
from .models import Genres, Directors, Films
from .schemas import GenresSchemaLoad, GenresSchema, DirectorsSchemaLoad, DirectorsSchema, \
    FilmsSchema, FilmsSchemaLoad, ValidateSchemas
from .utils import parse_films_json, filter_by_directors, filter_by_genre, \
    update_directors, update_genres

genres_schema_load = GenresSchemaLoad()
genres_schema = GenresSchema()
directors_schema_load = DirectorsSchemaLoad()
directors_schema = DirectorsSchema()
films_schema = FilmsSchema()
films_schema_load = FilmsSchemaLoad()


genres_model = api.model('Genres', {
    'genre_id': fields.Integer(readonly=True),
    'genre_name': fields.String(required=True),
})

directors_model = api.model('Directors', {
    'director_id': fields.Integer(readonly=True),
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'age': fields.Float(required=True)
})

films_model = api.model('Films', {
    'film_id': fields.Integer(readonly=True),
    'film_title': fields.String(required=True),
    'release_date': fields.Date(required=True),
    'description': fields.String(default='unknown'),
    'rate': fields.Float(required=True),
    'poster': fields.String(required=True),
    'directors': fields.List(fields.Nested(directors_model, required=True)),
    'genres': fields.List(fields.Nested(genres_model, required=True)),
})


@api.route('/genres')
class GenresListApi(Resource):

    @api.marshal_with(genres_model, as_list=True, code=200)
    def get(self):
        """
        Fetch list all genres
        """
        genres = Genres.query.all()
        return genres_schema.dump(genres, many=True)

    @api.expect(genres_model)
    @api.marshal_with(genres_model, code=201)
    @login_required
    def post(self):
        """
        Create a new genre
        """
        errors = ValidateSchemas.validate_genre(request.json)
        if errors:
            return abort(400, {'errors': errors})

        genre = genres_schema_load.load(request.json, session=db.session)
        db.session.add(genre)
        db.session.commit()
        return genres_schema.dump(genre)


@api.route('/genres/<genre_id>')
class GenresApi(Resource):

    @api.marshal_with(genres_model, code=200)
    def get(self, genre_id):
        """
        Fetch genre given its identifier
        """
        genre = Genres.query.filter_by(genre_id=genre_id).first()
        if genre is None:
            return {'message': "Genre not found"}, 404
        return genres_schema.dump(genre)

    @api.expect(genres_model)
    @api.marshal_with(genres_model, code=200)
    @login_required
    def put(self, genre_id):
        """
        Update genre given its identifier
        """
        errors = ValidateSchemas.validate_genre(request.json)
        if errors:
            return abort(400, {'errors': errors})

        genre = Genres.query.filter_by(genre_id=genre_id).first()
        if genre is None:
            return {'message': "Genre not found"}, 404
        genre = genres_schema_load.load(request.json, instance=genre, session=db.session)
        db.session.add(genre)
        db.session.commit()
        return genres_schema.dump(genre)

    @login_required
    def delete(self, genre_id):
        """
        Delete genre given its identifier
        """
        genre = Genres.query.filter_by(genre_id=genre_id).first()
        if genre is None:
            return {'message': "Genre not found"}, 404
        db.session.delete(genre)
        db.session.commit()
        return {}, 204


@api.route('/directors')
class DirectorsListApi(Resource):

    @api.marshal_with(directors_model, as_list=True)
    def get(self):
        """
        Fetch list of directors
        """
        directors = Directors.query.all()
        return directors_schema.dump(directors, many=True)

    @api.expect(directors_model)
    @api.marshal_with(directors_model, as_list=True)
    @login_required
    def post(self):
        """
        Create a new director
        """
        errors = ValidateSchemas.validate_director(request.json)
        if errors:
            return abort(400, {'errors': errors})

        director = directors_schema_load.load(request.json, session=db.session)
        db.session.add(director)
        db.session.commit()
        return directors_schema.dump(director)


@api.route('/directors/<director_id>')
class DirectorsApi(Resource):

    @api.marshal_with(directors_model, as_list=True)
    def get(self, director_id):
        """
        Fetch director given its identifier
        """
        director = Directors.query.filter_by(director_id=director_id).first()
        if director is None:
            return {'message': "Director not found"}, 404
        return directors_schema.dump(director)

    @api.expect(directors_model)
    @api.marshal_with(directors_model, as_list=True)
    @login_required
    def put(self, director_id):
        """
        Update director given its identifier
        """
        errors = ValidateSchemas.validate_director(request.json)
        if errors:
            return abort(400, {'errors': errors})

        director = Directors.query.filter_by(director_id=director_id).first()
        if director is None:
            return {'message': "Director not found"}, 404

        director = directors_schema_load.load(request.json, instance=director, session=db.session)
        db.session.add(director)
        db.session.commit()
        return directors_schema.dump(director)

    @login_required
    def delete(self, director_id):
        """
        Delete director given its identifier
        """
        director = Directors.query.filter_by(director_id=director_id).first()
        if director is None:
            return {'message': "Director not found"}, 404
        db.session.delete(director)
        db.session.commit()
        return {}, 204


@api.route('/films')
class FilmsListApi(Resource):

    @api.param('search', 'Search the film by partial or full coincidence. Case sensitive')
    @api.param('page', 'Number of page. Max per page 10 records')
    @api.param('start_date', 'Start date for filtering')
    @api.param('end_date', 'End date for filtering')
    @api.param('genre', 'Genre for filtering')
    @api.param('director', 'Director last name for filtering')
    @api.param('rate', 'Rate for filtering')
    @api.marshal_with(films_model, code=200)
    def get(self):
        """
        Fetch list of films
        """

        key_query = {'start_date', 'end_date', 'rate', 'genre', 'directors'}
        try:
            page = request.args.get('page', 1, type=int)
        except ValueError:
            page = 1

        if request.args.get('search', ''):
            films = Films.query.filter(Films.film_title.contains(request.args.get('search')))

        args = set(request.args.keys())
        args.discard('page')
        if not args:
            films = Films.query

        start_date = request.args.get('start_date', date(1971, 1, 1))
        end_date = request.args.get('end_date', date(9999, 12, 31))

        rate_start = 0
        rate_end = 10
        if request.args.get('rate'):
            rate_start = rate_end = request.args.get('rate')

        if key_query.intersection(set(request.args.keys())):
            genre = filter_by_genre(request.args)
            director = filter_by_directors(request.args)
            films = Films.query.join(Films.genres).filter(Genres.genre_name.in_(genre)).\
                filter(Films.release_date.between(start_date, end_date)).join(Films.directors).\
                filter(Directors.last_name.in_(director)).\
                filter(Films.rate.between(rate_start, rate_end))

        return films_schema.dump(films.paginate(page=page, per_page=10).items, many=True)

    @api.expect(films_model)
    @api.marshal_with(films_model, code=200)
    @login_required
    def post(self):
        """
        Create a new film
        """
        errors = ValidateSchemas.validate_films(request.json)
        if errors:
            return abort(400, {'errors': errors})

        input_ = parse_films_json(request.json)
        film = films_schema_load.load(input_, session=db.session, transient=True)

        film.directors = update_directors(request.json)
        film.genres = update_genres(request.json)
        film.users = current_user
        db.session.add(film)
        db.session.commit()
        return films_schema.dump(film)


@api.route('/films/<film_id>')
class FilmApi(Resource):

    @api.marshal_with(films_model, code=200)
    def get(self, film_id):
        """
        Fetch film given its identifier
        """
        film = Films.query.filter_by(film_id=film_id).first()
        if film is None:
            return {'message': "Film not found"}, 404
        return films_schema.dump(film)

    @api.expect(films_model)
    @api.marshal_with(films_model, code=200)
    @login_required
    def put(self, film_id):
        """
        Update film given its identifier
        """
        errors = ValidateSchemas.validate_films(request.json)
        if errors:
            return abort(400, {'errors': errors})

        film = Films.query.filter_by(film_id=film_id).first()
        if film is None:
            return {'message': "Film not found"}, 404
        film = films_schema_load.load(parse_films_json(request.json),
                                      instance=film, session=db.session)

        film.directors = update_directors(request.json)
        film.genres = update_genres(request.json)
        db.session.add(film)
        db.session.commit()
        return films_schema.dump(film)

    @login_required
    def delete(self, film_id):
        """
        Delete film given its identifier
        """
        film = Films.query.filter_by(film_id=film_id).first()
        if film is None:
            return {'message': "Film not found"}, 404
        db.session.delete(film)
        db.session.commit()
        return {}, 204