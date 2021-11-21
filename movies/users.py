# -*- coding: utf-8 -*-
"""
   Collect logic for users
"""

import logging
from typing import Dict, List, Tuple, Union
from flask import request, abort
from flask_restx import Resource, fields
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash
from . import api, db
from .schemas import UserSchema, ValidateSchemas
from .models import Users

logger = logging.getLogger('movies.users')

user_schema = UserSchema()

users_model = api.model('Users', {
    'user_id': fields.Integer(readonly=True),
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'age': fields.Integer(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'is_admin': fields.Boolean(required=True),
})

login_model = api.model('Login', {
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})


@api.route('/registration')
class UsersApi(Resource):
    """
    Shows a list of all users, and lets you POST to add new user
    """

    @api.marshal_with(users_model, code=200)
    def get(self) -> Tuple[Union[List[Users], List], int]:
        """
        Fetch list of users
        """
        users = Users.query.all()
        logger.info(f'User: {current_user} fetched all users: {users}')
        return user_schema.dump(users, many=True)

    @api.expect(users_model)
    @api.marshal_with(users_model, code=201)
    def post(self) -> Tuple[Union[Users, Dict], int]:
        """
        Create a new user
        """

        errors = ValidateSchemas.validate_user(request.json)
        if errors:
            logger.error(f'User: {current_user} entered wrong data {errors} for updating genre')
            return abort(400, {'errors': errors})

        user = Users.query.filter_by(email=request.json.get("email")).first()
        if user:
            logger.error('User entered existed email')
            return abort(409, f"User with email: {request.json.get('email')} exist")

        user = user_schema.load(request.json, session=db.session)
        db.session.add(user)
        db.session.commit()
        logger.info(f'User has created new user: {user}')
        return user_schema.dump(user), 201


@api.route('/registration/<email>')
class UserApi(Resource):
    """
    Lets you delete or update user
    """
    @api.expect(users_model)
    @api.marshal_with(users_model, code=200)
    def put(self, email: str) -> Tuple[Union[Users, Dict], int]:
        """
        Update user's data
        """
        errors = ValidateSchemas.validate_user(request.json)
        if errors:
            logger.error(f'User: {current_user} entered wrong data {errors} for updating user')
            return abort(400, {'errors': errors})

        user = Users.query.filter_by(email=email).first()
        if user is None:
            logger.error(f'User: {current_user} entered non-existent user email: {email}')
            return abort(404, f"User with email: {email} not found")

        user = user_schema.load(request.json, instance=user, session=db.session)
        db.session.add(user)
        db.session.commit()
        logger.info(f'User: {current_user} updated {user}')
        return user_schema.dump(user), 200

    def delete(self, email: str) -> Tuple[Union[Users, Dict], int]:
        """
        Delete user given its email
        """
        user = Users.query.filter_by(email=email).first()
        if user is None:
            return abort(404, f"User with email: {email} not found")
        db.session.delete(user)
        db.session.commit()
        logger.info(f'User: {current_user} deleted {user}')
        return {}, 204


@api.route('/login')
class UserLogin(Resource):
    """
    Lets you login to app
    """

    @api.expect(login_model)
    @api.marshal_with(login_model, code=200)
    def post(self) -> Dict:
        """
        User authorization
        """

        if current_user.is_authenticated:
            return {"message": f"User with email: {request.json.get('email')} has been auth"}

        user = Users.query.filter_by(email=request.json.get('email')).first()
        if user and check_password_hash(user.password, request.json.get('password')):
            login_user(user, remember=True)
            logger.info(f"User with email: {request.json.get('email')} is logged in")
            return {"message": f"User with email: {request.json.get('email')} is logged in"}
        return {"message": "Wrong credentials"}


@api.route('/logout')
class UserLogout(Resource):
    """
    Lets you logout from app
    """
    def get(self) -> Dict[str, str]:
        """
        Logout from API
        """
        logout_user()
        logger.info('Current user is logged out')
        return {"message": "Current user is logged out"}
