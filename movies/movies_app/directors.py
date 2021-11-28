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
from movies.models import Directors
from movies.schemas import DirectorsSchemaLoad, DirectorsSchema, ValidateSchemas


logger = logging.getLogger("movies.movies_app.directors")


directors_schema_load = DirectorsSchemaLoad()
directors_schema = DirectorsSchema()


directors_model = api.model("Directors", {
    "director_id": fields.Integer(readonly=True),
    "first_name": fields.String(required=True),
    "last_name": fields.String(required=True),
    "age": fields.Float(required=True)
})


@api.route("/directors")
class DirectorsListApi(Resource):
    """
    Shows a list of all directors, and lets you POST to add new director
    """
    @api.marshal_with(directors_model, as_list=True)
    def get(self) -> Tuple[Union[List[Directors], List], int]:
        """
        Fetch list of directors
        """
        directors = Directors.query.all()
        logger.info(f"User: {current_user} fetched list all directors: {directors}")
        return directors_schema.dump(directors, many=True), 200

    @api.expect(directors_model)
    @api.marshal_with(directors_model, code=201)
    @login_required
    def post(self) -> Tuple[Union[Directors, Dict], int]:
        """
        Create a new director
        """
        errors = ValidateSchemas.validate_director(request.json)
        if errors:
            logger.error(f"User: {current_user} entered wrong data {errors} for creating director")
            return abort(400, {"errors": errors})

        director = directors_schema_load.load(request.json, session=db.session)
        db.session.add(director)
        db.session.commit()
        logger.info(f"User: {current_user} has created a new director: {director}")
        return directors_schema.dump(director), 201


@api.route("/directors/<director_id>")
class DirectorsApi(Resource):
    """
    Show a single director item and lets you delete or update them
    """
    @api.marshal_with(directors_model, as_list=True)
    def get(self, director_id: int) -> Tuple[Union[Directors, Dict], int]:
        """
        Fetch director given its identifier
        """
        director = Directors.query.filter_by(director_id=director_id).first()
        if director is None:
            logger.error(f"User: {current_user} entered non-existent director id: {director_id}")
            return abort(404, "Director not found")
        logger.info(f"User: {current_user} fetched {director}")
        return directors_schema.dump(director), 200

    @api.expect(directors_model)
    @api.marshal_with(directors_model, as_list=True, code=200)
    @login_required
    def put(self, director_id: int) -> Tuple[Union[Directors, Dict], int]:
        """
        Update director given its identifier
        """
        errors = ValidateSchemas.validate_director(request.json)
        if errors:
            logger.error(f"User: {current_user} entered wrong data {errors} for updating director")
            return abort(400, {"errors": errors})

        director = Directors.query.filter_by(director_id=director_id).first()
        if director is None:
            logger.error(f"User: {current_user} entered non-existent director id: {director_id}")
            return abort(404, "Director not found")

        director = directors_schema_load.load(request.json, instance=director, session=db.session)
        db.session.add(director)
        db.session.commit()
        logger.info(f"User: {current_user} updated {director}")
        return directors_schema.dump(director), 200

    @login_required
    def delete(self, director_id: int) -> Tuple[Dict, int]:
        """
        Delete director given its identifier
        """
        director = Directors.query.filter_by(director_id=director_id).first()
        if director is None:
            logger.error(f"User: {current_user} entered non-existent director id: {director_id}")
            return abort(404, "Director not found")
        db.session.delete(director)
        db.session.commit()
        logger.info(f"User: {current_user} deleted {director}")
        return {}, 204
