# -*- coding: utf-8 -*-
"""
   Collect all routes to films, genres and directors
"""

from datetime import date
import logging
from typing import Dict, List, Tuple, Union
from flask import request, abort
from flask_restx import Resource, fields
from flask_login import login_required, current_user
from movies import api, db
from movies.models import Genres, Directors, Films
from movies.schemas import FilmsSchema, FilmsSchemaLoad, ValidateSchemas
from movies.movies_app.utils import parse_films_json, filter_by_directors, filter_by_genre, \
    update_directors, update_genres
from .genres import genres_model
from .directors import directors_model

logger = logging.getLogger("movies.movies_app.routes")

films_schema = FilmsSchema()
films_schema_load = FilmsSchemaLoad()

films_model = api.model("Films", {
    "film_id": fields.Integer(readonly=True),
    "film_title": fields.String(required=True),
    "release_date": fields.Date(required=True),
    "description": fields.String(default="unknown"),
    "rate": fields.Float(required=True),
    "poster": fields.String(required=True),
    "directors": fields.List(fields.Nested(directors_model, required=True)),
    "genres": fields.List(fields.Nested(genres_model, required=True)),
})


@api.route("/films")
class FilmsListApi(Resource):
    """
    Shows a list of all films, and lets you POST to add new film
    """

    @api.param("search", "Search the film by partial or full coincidence title. Case sensitive")
    @api.param("page", "Number of page. Max per page 10 records")
    @api.param("start_date", "Start date for filtering. Format should be 'YYYY-MM-DD'."
                             " For example '1971-01-01'")
    @api.param("end_date", "End date for filtering. Format should be 'YYYY-MM-DD'. "
                           "For example '1971-01-01'")
    @api.param("genre", "Genre for filtering.")
    @api.param("director", "Director last name for filtering")
    @api.param("rate", "Rate for filtering. Should be float")
    @api.marshal_with(films_model, code=200)
    def get(self) -> Tuple[Union[List[Films], List], int]:
        """
        Fetch list of films. Params: "start_date", "end_date", "rate", "genre", "director"
        can be combined together. Search param work alone.
        If all params empty query return 10 films.
        """

        key_query = {"start_date", "end_date", "rate", "genre", "director"}
        try:
            page = request.args.get("page", 1, type=int)
        except ValueError:
            page = 1

        if request.args.get("search", ""):
            films = Films.query.filter(Films.film_title.contains(request.args.get("search")))

        args = set(request.args.keys())
        args.discard("page")
        if not args:
            films = Films.query

        start_date = request.args.get("start_date", date(1971, 1, 1))
        end_date = request.args.get("end_date", date(9999, 12, 31))

        rate_start = 0
        rate_end = 10
        if request.args.get("rate"):
            rate_start = rate_end = request.args.get("rate")

        if key_query.intersection(set(request.args.keys())):
            genre = filter_by_genre(request.args)
            director = filter_by_directors(request.args)
            films = Films.query.join(Films.genres).filter(Genres.genre_name.in_(genre)).\
                filter(Films.release_date.between(start_date, end_date)).join(Films.directors).\
                filter(Directors.last_name.in_(director)).\
                filter(Films.rate.between(rate_start, rate_end))
        logger.info(f"User: {current_user} fetched films: {films}")
        return films_schema.dump(films.paginate(page=page, per_page=10).items, many=True)

    @api.expect(films_model)
    @api.marshal_with(films_model, code=201)
    @login_required
    def post(self) -> Tuple[Union[Films, Dict], int]:
        """
        Create a new film
        """
        errors = ValidateSchemas.validate_films(request.json)
        if errors:
            logger.error(f"User: {current_user} entered wrong data {errors} for creating film")
            return abort(400, {"errors": errors})

        input_ = parse_films_json(request.json)
        film = films_schema_load.load(input_, session=db.session, transient=True)

        film.directors = update_directors(request.json)
        film.genres = update_genres(request.json)
        film.users = current_user
        db.session.add(film)
        db.session.commit()
        logger.info(f"User: {current_user} has created a new film: {film}")
        return films_schema.dump(film), 201


@api.route("/films/<film_id>")
class FilmApi(Resource):
    """
    Show a single film item and lets you delete or update them
    """

    @api.marshal_with(films_model, code=200)
    def get(self, film_id: int) -> Tuple[Union[Films, Dict], int]:
        """
        Fetch film given its identifier
        """
        film = Films.query.filter_by(film_id=film_id).first()
        if film is None:
            logger.error(f"User: {current_user} entered non-existent film id: {film_id}")
            return abort(404, "Film not found")

        logger.info(f"User: {current_user} fetched {film}")
        return films_schema.dump(film), 200

    @api.expect(films_model)
    @api.marshal_with(films_model, code=200)
    @login_required
    def put(self, film_id: int) -> Tuple[Union[Directors, Dict], int]:
        """
        Update film given its identifier
        """
        errors = ValidateSchemas.validate_films(request.json)
        if errors:
            logger.error(f"User: {current_user} entered wrong data {errors} for updating film")
            return abort(400, {"errors": errors})

        film = Films.query.filter_by(film_id=film_id).first()
        if film is None:
            logger.error(f"User: {current_user} entered non-existent film id: {film_id}")
            return abort(404, "Film not found")
        if not (current_user.is_admin or film.users.email == current_user.email):
            return abort(403, f"User with email: {current_user.email} is not "
                              f"admin or did not create this film")

        film = films_schema_load.load(parse_films_json(request.json),
                                      instance=film, session=db.session)

        film.directors = update_directors(request.json)
        film.genres = update_genres(request.json)
        db.session.add(film)
        db.session.commit()
        logger.info(f"User: {current_user} updated {film}")
        return films_schema.dump(film), 200

    @login_required
    def delete(self, film_id: int) -> Tuple[Dict, int]:
        """
        Delete film given its identifier
        """
        film = Films.query.filter_by(film_id=film_id).first()
        if film is None:
            logger.error(f"User: {current_user} entered non-existent film id: {film_id}")
            return abort(404, "Film not found")

        if not (current_user.is_admin or film.users.email == current_user.email):
            return abort(403, f"User with email: {current_user.email} is not "
                              f"admin or did not create this film")

        db.session.delete(film)
        db.session.commit()
        logger.info(f"User: {current_user} deleted {film}")
        return {}, 204
