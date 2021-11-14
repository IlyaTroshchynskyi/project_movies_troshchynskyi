from flask import request
from flask_restx import Resource, fields
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash
from . import api, db
from .schemas import UserSchema
from .models import Users

user_schema = UserSchema()

users_model = api.model('Users', {
    'user_id': fields.Integer(readonly=True),
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'age': fields.Float(required=True),
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

    @api.marshal_with(users_model, code=200)
    def get(self):
        """
        Fetch list of users
        """
        users = Users.query.all()
        return user_schema.dump(users, many=True)

    @api.expect(users_model)
    @api.marshal_with(users_model, code=201)
    def post(self):
        """
        Create a new user
        """

        user = Users.query.filter_by(email=request.json.get("email")).first()
        if user:
            return {"message": f"User with email: {request.json.get('email')} exist"}
        user = user_schema.load(request.json, session=db.session)
        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user), 201


@api.route('/registration/<email>')
class UserApi(Resource):

    @api.expect(users_model)
    @api.marshal_with(users_model, 200)
    def put(self, email):
        """
        Update user's data
        """
        user = Users.query.filter_by(email=email).first()
        if user is None:
            return {"message": f"User with email: {email} not found"}, 404
        user = user_schema.load(request.json, instance=user, session=db.session)
        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user), 200

    def delete(self, email):
        """
        Delete user given its email
        """
        user = Users.query.filter_by(email=email).first()
        if user is None:
            return {"message": f"User with email: {email} not found"}, 404
        db.session.delete(user)
        db.session.commit()
        return {}, 204


@api.route('/login')
class UserLogin(Resource):

    @api.expect(login_model)
    @api.marshal_with(users_model)
    def post(self):
        """
        User authorization
        """
        if current_user.is_authenticated:
            return {"message": f"User with email: {request.json.get('email')} has been auth"}

        user = Users.query.filter_by(email=request.json.get('email')).first()
        if user and check_password_hash(user.password, request.json.get('password')):
            login_user(user, remember=True)
            return {"message": f"User with email: {request.json.get('email')} is logged in"}
        return {"message": f"Wrong credentials"}


@api.route('/logout')
class UserLogin(Resource):

    def get(self):
        """
        Logout from API
        """
        logout_user()
        return {"message": f"Current user is logged out"}