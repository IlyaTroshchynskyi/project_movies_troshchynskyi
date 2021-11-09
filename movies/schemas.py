from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from .models import Genres


class GenresSchemaLoad(SQLAlchemyAutoSchema):
    class Meta:
        model = Genres
        load_instance = True


class GenresSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Genres

