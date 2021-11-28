# # -*- coding: utf-8 -*-
# """
#    Collect all routes to films, genres and directors
# """
#
# from datetime import date
# import logging
# from typing import Dict, List, Tuple, Union
# from flask import request, abort
# from flask_restx import Resource, fields
# from flask_login import login_required, current_user
# from movies import api, db
# from movies.models import Genres, Directors, Films
# from movies.schemas import GenresSchemaLoad, GenresSchema, DirectorsSchemaLoad, DirectorsSchema, \
#     FilmsSchema, FilmsSchemaLoad, ValidateSchemas
# from movies.utils import parse_films_json, filter_by_directors, filter_by_genre, \
#     update_directors, update_genres
#
#
# logger = logging.getLogger("movies.routes")
#
# genres_schema_load = GenresSchemaLoad()
# genres_schema = GenresSchema()
# directors_schema_load = DirectorsSchemaLoad()
# directors_schema = DirectorsSchema()
# films_schema = FilmsSchema()
# films_schema_load = FilmsSchemaLoad()
#
#
# genres_model = api.model("Genres", {
#     "genre_id": fields.Integer(readonly=True),
#     "genre_name": fields.String(required=True),
# })
#
# directors_model = api.model("Directors", {
#     "director_id": fields.Integer(readonly=True),
#     "first_name": fields.String(required=True),
#     "last_name": fields.String(required=True),
#     "age": fields.Float(required=True)
# })
#
# films_model = api.model("Films", {
#     "film_id": fields.Integer(readonly=True),
#     "film_title": fields.String(required=True),
#     "release_date": fields.Date(required=True),
#     "description": fields.String(default="unknown"),
#     "rate": fields.Float(required=True),
#     "poster": fields.String(required=True),
#     "directors": fields.List(fields.Nested(directors_model, required=True)),
#     "genres": fields.List(fields.Nested(genres_model, required=True)),
# })
#
#
# @api.route("/genres")
# class GenresListApi(Resource):
#     """
#     Shows a list of all genres, and lets you POST to add new genre
#     """
#
#     @api.marshal_with(genres_model, as_list=True, code=200)
#     def get(self) -> Tuple[Union[List[Genres], List], int]:
#         """
#         Fetch list all genres
#         """
#         genres = Genres.query.all()
#         logger.info(f"User: {current_user} fetched list all genres: {genres}")
#         return genres_schema.dump(genres, many=True), 200
#
#     @api.expect(genres_model)
#     @api.marshal_with(genres_model, code=201)
#     @login_required
#     def post(self) -> Tuple[Union[Genres, Dict], int]:
#         """
#         Create a new genre
#         """
#         errors = ValidateSchemas.validate_genre(request.json)
#         if errors:
#             logger.error(f"User: {current_user} entered wrong data {errors} for creating genre")
#             return abort(400, {"errors": errors})
#
#         genre = genres_schema_load.load(request.json, session=db.session)
#         db.session.add(genre)
#         db.session.commit()
#         logger.info(f"User: {current_user} has created new genre: {genre}")
#         return genres_schema.dump(genre), 201
#
#
# @api.route("/genres/<genre_id>")
# class GenresApi(Resource):
#     """
#     Show a single genre item and lets you delete or update them
#     """
#     @api.marshal_with(genres_model, code=200)
#     def get(self, genre_id: int) -> Tuple[Union[Genres, Dict], int]:
#         """
#         Fetch genre given its identifier
#         """
#         genre = Genres.query.filter_by(genre_id=genre_id).first()
#         if genre is None:
#             logger.error(f"User: {current_user} entered non-existent genre id: {genre_id}")
#             return abort(404, "Genre not found")
#         logger.info(f"User: {current_user} fetched {genre}")
#         return genres_schema.dump(genre), 200
#
#     @api.expect(genres_model)
#     @api.marshal_with(genres_model, code=200)
#     @login_required
#     def put(self, genre_id: int) -> Tuple[Union[Genres, Dict], int]:
#         """
#         Update genre given its identifier
#         """
#         errors = ValidateSchemas.validate_genre(request.json)
#         if errors:
#             logger.error(f"User: {current_user} entered wrong data {errors} for updating genre")
#             return abort(400, {"errors": errors})
#
#         genre = Genres.query.filter_by(genre_id=genre_id).first()
#         if genre is None:
#             logger.error(f"User: {current_user} entered non-existent genre id: {genre_id}")
#             return abort(404, "Genre not found")
#         genre = genres_schema_load.load(request.json, instance=genre, session=db.session)
#         db.session.add(genre)
#         db.session.commit()
#         logger.info(f"User: {current_user} updated {genre}")
#         return genres_schema.dump(genre)
#
#     @login_required
#     def delete(self, genre_id: int) -> Tuple[Dict, int]:
#         """
#         Delete genre given its identifier
#         """
#         genre = Genres.query.filter_by(genre_id=genre_id).first()
#         if genre is None:
#             logger.error(f"User: {current_user} entered non-existent genre id: {genre_id}")
#             return abort(404, "Genre not found")
#         db.session.delete(genre)
#         db.session.commit()
#         logger.info(f"User: {current_user} deleted {genre}")
#         return {}, 204
#
#
# @api.route("/directors")
# class DirectorsListApi(Resource):
#     """
#     Shows a list of all directors, and lets you POST to add new director
#     """
#     @api.marshal_with(directors_model, as_list=True)
#     def get(self) -> Tuple[Union[List[Directors], List], int]:
#         """
#         Fetch list of directors
#         """
#         directors = Directors.query.all()
#         logger.info(f"User: {current_user} fetched list all directors: {directors}")
#         return directors_schema.dump(directors, many=True), 200
#
#     @api.expect(directors_model)
#     @api.marshal_with(directors_model, code=201)
#     @login_required
#     def post(self) -> Tuple[Union[Directors, Dict], int]:
#         """
#         Create a new director
#         """
#         errors = ValidateSchemas.validate_director(request.json)
#         if errors:
#             logger.error(f"User: {current_user} entered wrong data {errors} for creating director")
#             return abort(400, {"errors": errors})
#
#         director = directors_schema_load.load(request.json, session=db.session)
#         db.session.add(director)
#         db.session.commit()
#         logger.info(f"User: {current_user} has created a new director: {director}")
#         return directors_schema.dump(director), 201
#
#
# @api.route("/directors/<director_id>")
# class DirectorsApi(Resource):
#     """
#     Show a single director item and lets you delete or update them
#     """
#     @api.marshal_with(directors_model, as_list=True)
#     def get(self, director_id: int) -> Tuple[Union[Directors, Dict], int]:
#         """
#         Fetch director given its identifier
#         """
#         director = Directors.query.filter_by(director_id=director_id).first()
#         if director is None:
#             logger.error(f"User: {current_user} entered non-existent director id: {director_id}")
#             return abort(404, "Director not found")
#         logger.info(f"User: {current_user} fetched {director}")
#         return directors_schema.dump(director), 200
#
#     @api.expect(directors_model)
#     @api.marshal_with(directors_model, as_list=True, code=200)
#     @login_required
#     def put(self, director_id: int) -> Tuple[Union[Directors, Dict], int]:
#         """
#         Update director given its identifier
#         """
#         errors = ValidateSchemas.validate_director(request.json)
#         if errors:
#             logger.error(f"User: {current_user} entered wrong data {errors} for updating director")
#             return abort(400, {"errors": errors})
#
#         director = Directors.query.filter_by(director_id=director_id).first()
#         if director is None:
#             logger.error(f"User: {current_user} entered non-existent director id: {director_id}")
#             return abort(404, "Director not found")
#
#         director = directors_schema_load.load(request.json, instance=director, session=db.session)
#         db.session.add(director)
#         db.session.commit()
#         logger.info(f"User: {current_user} updated {director}")
#         return directors_schema.dump(director), 200
#
#     @login_required
#     def delete(self, director_id: int) -> Tuple[Dict, int]:
#         """
#         Delete director given its identifier
#         """
#         director = Directors.query.filter_by(director_id=director_id).first()
#         if director is None:
#             logger.error(f"User: {current_user} entered non-existent director id: {director_id}")
#             return abort(404, "Director not found")
#         db.session.delete(director)
#         db.session.commit()
#         logger.info(f"User: {current_user} deleted {director}")
#         return {}, 204
#
#
# @api.route("/films")
# class FilmsListApi(Resource):
#     """
#     Shows a list of all films, and lets you POST to add new film
#     """
#
#     @api.param("search", "Search the film by partial or full coincidence title. Case sensitive")
#     @api.param("page", "Number of page. Max per page 10 records")
#     @api.param("start_date", "Start date for filtering. Format should be 'YYYY-MM-DD'."
#                              " For example '1971-01-01'")
#     @api.param("end_date", "End date for filtering. Format should be 'YYYY-MM-DD'. "
#                            "For example '1971-01-01'")
#     @api.param("genre", "Genre for filtering.")
#     @api.param("director", "Director last name for filtering")
#     @api.param("rate", "Rate for filtering. Should be float")
#     @api.marshal_with(films_model, code=200)
#     def get(self) -> Tuple[Union[List[Films], List], int]:
#         """
#         Fetch list of films. Params: "start_date", "end_date", "rate", "genre", "director"
#         can be combined together. Search param work alone.
#         If all params empty query return 10 films.
#         """
#
#         key_query = {"start_date", "end_date", "rate", "genre", "director"}
#         try:
#             page = request.args.get("page", 1, type=int)
#         except ValueError:
#             page = 1
#
#         if request.args.get("search", ""):
#             films = Films.query.filter(Films.film_title.contains(request.args.get("search")))
#
#         args = set(request.args.keys())
#         args.discard("page")
#         if not args:
#             films = Films.query
#
#         start_date = request.args.get("start_date", date(1971, 1, 1))
#         end_date = request.args.get("end_date", date(9999, 12, 31))
#
#         rate_start = 0
#         rate_end = 10
#         if request.args.get("rate"):
#             rate_start = rate_end = request.args.get("rate")
#
#         if key_query.intersection(set(request.args.keys())):
#             genre = filter_by_genre(request.args)
#             director = filter_by_directors(request.args)
#             films = Films.query.join(Films.genres).filter(Genres.genre_name.in_(genre)).\
#                 filter(Films.release_date.between(start_date, end_date)).join(Films.directors).\
#                 filter(Directors.last_name.in_(director)).\
#                 filter(Films.rate.between(rate_start, rate_end))
#         logger.info(f"User: {current_user} fetched films: {films}")
#         return films_schema.dump(films.paginate(page=page, per_page=10).items, many=True)
#
#     @api.expect(films_model)
#     @api.marshal_with(films_model, code=201)
#     @login_required
#     def post(self) -> Tuple[Union[Films, Dict], int]:
#         """
#         Create a new film
#         """
#         errors = ValidateSchemas.validate_films(request.json)
#         if errors:
#             logger.error(f"User: {current_user} entered wrong data {errors} for creating film")
#             return abort(400, {"errors": errors})
#
#         input_ = parse_films_json(request.json)
#         film = films_schema_load.load(input_, session=db.session, transient=True)
#
#         film.directors = update_directors(request.json)
#         film.genres = update_genres(request.json)
#         film.users = current_user
#         db.session.add(film)
#         db.session.commit()
#         logger.info(f"User: {current_user} has created a new film: {film}")
#         return films_schema.dump(film), 201
#
#
# @api.route("/films/<film_id>")
# class FilmApi(Resource):
#     """
#     Show a single film item and lets you delete or update them
#     """
#
#     @api.marshal_with(films_model, code=200)
#     def get(self, film_id: int) -> Tuple[Union[Films, Dict], int]:
#         """
#         Fetch film given its identifier
#         """
#         film = Films.query.filter_by(film_id=film_id).first()
#         if film is None:
#             logger.error(f"User: {current_user} entered non-existent film id: {film_id}")
#             return abort(404, "Film not found")
#
#         logger.info(f"User: {current_user} fetched {film}")
#         return films_schema.dump(film), 200
#
#     @api.expect(films_model)
#     @api.marshal_with(films_model, code=200)
#     @login_required
#     def put(self, film_id: int) -> Tuple[Union[Directors, Dict], int]:
#         """
#         Update film given its identifier
#         """
#         errors = ValidateSchemas.validate_films(request.json)
#         if errors:
#             logger.error(f"User: {current_user} entered wrong data {errors} for updating film")
#             return abort(400, {"errors": errors})
#
#         film = Films.query.filter_by(film_id=film_id).first()
#         if film is None:
#             logger.error(f"User: {current_user} entered non-existent film id: {film_id}")
#             return abort(404, "Film not found")
#         if not (current_user.is_admin or film.users.email == current_user.email):
#             return abort(403, f"User with email: {current_user.email} is not "
#                               f"admin or did not create this film")
#
#         film = films_schema_load.load(parse_films_json(request.json),
#                                       instance=film, session=db.session)
#
#         film.directors = update_directors(request.json)
#         film.genres = update_genres(request.json)
#         db.session.add(film)
#         db.session.commit()
#         logger.info(f"User: {current_user} updated {film}")
#         return films_schema.dump(film), 200
#
#     @login_required
#     def delete(self, film_id: int) -> Tuple[Dict, int]:
#         """
#         Delete film given its identifier
#         """
#         film = Films.query.filter_by(film_id=film_id).first()
#         if film is None:
#             logger.error(f"User: {current_user} entered non-existent film id: {film_id}")
#             return abort(404, "Film not found")
#
#         if not (current_user.is_admin or film.users.email == current_user.email):
#             return abort(403, f"User with email: {current_user.email} is not "
#                               f"admin or did not create this film")
#
#         db.session.delete(film)
#         db.session.commit()
#         logger.info(f"User: {current_user} deleted {film}")
#         return {}, 204
