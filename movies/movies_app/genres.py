# -*- coding: utf-8 -*-
"""
   Collect all routes to films, genres and directors
"""

import logging
from typing import Dict, List, Tuple, Union
from flask import request, abort
from flask_restx import Resource, fields
from flask_login import login_required, current_user
from movies import api, db
from movies.models import Genres
from movies.schemas import GenresSchemaLoad, GenresSchema, ValidateSchemas


logger = logging.getLogger("movies.movies_app.genres")

genres_schema_load = GenresSchemaLoad()
genres_schema = GenresSchema()


genres_model = api.model("Genres", {
    "genre_id": fields.Integer(readonly=True),
    "genre_name": fields.String(required=True),
})


@api.route("/genres")
class GenresListApi(Resource):
    """
    Shows a list of all genres, and lets you POST to add new genre
    """

    @api.marshal_with(genres_model, as_list=True, code=200)
    def get(self) -> Tuple[Union[List[Genres], List], int]:
        """
        Fetch list all genres
        """
        genres = Genres.query.all()
        logger.info(f"User: {current_user} fetched list all genres: {genres}")
        return genres_schema.dump(genres, many=True), 200

    @api.expect(genres_model)
    @api.marshal_with(genres_model, code=201)
    @login_required
    def post(self) -> Tuple[Union[Genres, Dict], int]:
        """
        Create a new genre
        """
        errors = ValidateSchemas.validate_genre(request.json)
        if errors:
            logger.error(f"User: {current_user} entered wrong data {errors} for creating genre")
            return abort(400, {"errors": errors})

        genre = genres_schema_load.load(request.json, session=db.session)
        db.session.add(genre)
        db.session.commit()
        logger.info(f"User: {current_user} has created new genre: {genre}")
        return genres_schema.dump(genre), 201


@api.route("/genres/<genre_id>")
class GenresApi(Resource):
    """
    Show a single genre item and lets you delete or update them
    """
    @api.marshal_with(genres_model, code=200)
    def get(self, genre_id: int) -> Tuple[Union[Genres, Dict], int]:
        """
        Fetch genre given its identifier
        """
        genre = Genres.query.filter_by(genre_id=genre_id).first()
        if genre is None:
            logger.error(f"User: {current_user} entered non-existent genre id: {genre_id}")
            return abort(404, "Genre not found")
        logger.info(f"User: {current_user} fetched {genre}")
        return genres_schema.dump(genre), 200

    @api.expect(genres_model)
    @api.marshal_with(genres_model, code=200)
    @login_required
    def put(self, genre_id: int) -> Tuple[Union[Genres, Dict], int]:
        """
        Update genre given its identifier
        """
        errors = ValidateSchemas.validate_genre(request.json)
        if errors:
            logger.error(f"User: {current_user} entered wrong data {errors} for updating genre")
            return abort(400, {"errors": errors})

        genre = Genres.query.filter_by(genre_id=genre_id).first()
        if genre is None:
            logger.error(f"User: {current_user} entered non-existent genre id: {genre_id}")
            return abort(404, "Genre not found")
        genre = genres_schema_load.load(request.json, instance=genre, session=db.session)
        db.session.add(genre)
        db.session.commit()
        logger.info(f"User: {current_user} updated {genre}")
        return genres_schema.dump(genre)

    @login_required
    def delete(self, genre_id: int) -> Tuple[Dict, int]:
        """
        Delete genre given its identifier
        """
        genre = Genres.query.filter_by(genre_id=genre_id).first()
        if genre is None:
            logger.error(f"User: {current_user} entered non-existent genre id: {genre_id}")
            return abort(404, "Genre not found")
        db.session.delete(genre)
        db.session.commit()
        logger.info(f"User: {current_user} deleted {genre}")
        return {}, 204
