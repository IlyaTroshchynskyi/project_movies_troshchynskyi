from flask import request
from flask_restx import Resource
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash
from . import api, db
from .schemas import UserSchema
from .models import Users

user_schema = UserSchema()


@api.route('/registration')
class UserRegistration(Resource):

    user_schema = UserSchema()

    def get(self):

        users = Users.query.all()
        return self.user_schema.dump(users, many=True)

    def post(self):
        user = Users.query.filter_by(email=request.json.get("email")).first()
        if user:
            return {"message": f"User with email: {request.json.get('email')} exist"}
        user = self.user_schema.load(request.json, session=db.session)
        db.session.add(user)
        db.session.commit()
        return self.user_schema.dump(user), 201

    def put(self):
        user = Users.query.filter_by(email=request.json.get("email")).first()
        if user is None:
            return {"message": f"User with email: {request.json.get('email')} not found"}, 404
        user = self.user_schema.load(request.json, instance=user, session=db.session)
        db.session.add(user)
        db.session.commit()
        return self.user_schema.dump(user), 200

    def delete(self):
        user = Users.query.filter_by(email=request.json.get("email")).first()
        if user is None:
            return {"message": f"User with email: {request.json.get('email')} not found"}, 404
        db.session.delete(user)
        db.session.commit()
        return {}, 204


@api.route('/login')
class UserLogin(Resource):

    def post(self):
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
        logout_user()
        return {"message": f"Current user is logged out"}