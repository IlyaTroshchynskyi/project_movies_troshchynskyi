from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from .models import Genres, Directors


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
