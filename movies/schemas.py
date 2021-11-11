from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from .models import Genres, Directors, Films, Users
from marshmallow_sqlalchemy.fields import Nested


class GenresSchemaLoad(SQLAlchemyAutoSchema):
    class Meta:
        model = Genres
        load_instance = True


class GenresSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Genres


class DirectorsSchemaLoad(SQLAlchemyAutoSchema):
    class Meta:
        model = Directors
        load_instance = True


class DirectorsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Directors


class FilmsSchemaLoad(SQLAlchemyAutoSchema):
    class Meta:
        model = Films
        load_instance = True

    genres = Nested(GenresSchema, many=True)
    directors = Nested(DirectorsSchema, many=True)


class FilmsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Films

    genres = Nested(GenresSchema, many=True)
    directors = Nested(DirectorsSchema, many=True)


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        load_instance = True
        load_only = ('password',)