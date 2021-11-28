# -*- coding: utf-8 -*-
"""
   Collect all schemas
"""

import logging
from datetime import datetime
import re
from typing import Dict, Any, List
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested
from .models import Genres, Directors, Films, Users


logger = logging.getLogger("movies.schemas")


class GenresSchemaLoad(SQLAlchemyAutoSchema):
    """
     Class for loading an instance
    """
    class Meta:
        model = Genres
        load_instance = True


class GenresSchema(SQLAlchemyAutoSchema):
    """
    Class define the output
    """
    class Meta:
        model = Genres


class DirectorsSchemaLoad(SQLAlchemyAutoSchema):
    """
    Class for loading an instance
    """
    class Meta:
        model = Directors
        load_instance = True


class DirectorsSchema(SQLAlchemyAutoSchema):
    """
    Class define the output
    """
    class Meta:
        model = Directors


class FilmsSchemaLoad(SQLAlchemyAutoSchema):
    """
    Class for loading an instance
    """
    class Meta:
        model = Films
        load_instance = True

    genres = Nested(GenresSchema, many=True)
    directors = Nested(DirectorsSchema, many=True)


class FilmsSchema(SQLAlchemyAutoSchema):
    """
    Class define the output
    """
    class Meta:
        model = Films

    genres = Nested(GenresSchema, many=True)
    directors = Nested(DirectorsSchema, many=True)


class UserSchema(SQLAlchemyAutoSchema):
    """
    Class define the output
    """
    class Meta:
        model = Users
        load_instance = True
        load_only = ("password",)


class ValidateSchemas:
    """
    Schema for data validation
    """

    @staticmethod
    def validate_first_last_name_or_genre_length(data: str) -> bool:
        """
        Check length of first name, last name director and user or genre name
        """
        if len(str(data)) > 100 or len(str(data)) < 3:
            return True
        return False

    @staticmethod
    def validate_first_last_name_or_genre_string(data: str) -> bool:
        """
        Check that first name, last name director and user or genre name don"t contains numbers.
        """
        if re.search("[0-9]", str(data)):
            return True
        return False

    @classmethod
    def validate_genre(cls, data: Dict[str, Any]) -> List[str]:
        """
        Validate data for genre
        """
        errors = []
        try:
            if cls.validate_first_last_name_or_genre_length(data.get("genre_name", "")):
                errors.append("Length should be between 3 and 100 characters")
            if cls.validate_first_last_name_or_genre_string(data.get("genre_name", "")):
                errors.append("The genre should be string")
        except Exception as ex:
            logger.error(ex)
        return errors

    @classmethod
    def validate_director(cls, data: Dict[str, Any]) -> List[str]:
        """
        Validate data for director
        """
        errors = []

        try:
            if cls.validate_first_last_name_or_genre_length(data.get("first_name", "")):
                errors.append("Length first name should be between 3 and 100 characters")
            if cls.validate_first_last_name_or_genre_string(data.get("first_name", "")):
                errors.append("The first name should be string")

            if cls.validate_first_last_name_or_genre_length(data.get("last_name", "")):
                errors.append("Length last name should be between 3 and 100 characters")
            if cls.validate_first_last_name_or_genre_string(data.get("last_name", "")):
                errors.append("The last name should be string")

            if re.search("[A-Za-z]", str(data.get("age", ""))):
                errors.append("Age should be numeric")
            if data.get("age", 0) < 18:
                errors.append("The age should be more than 17")
            if str(data.get("age", "")).find(".") != -1:
                errors.append("The age should be numeric not float")

        except Exception as ex:
            logger.error(ex)
        return errors

    @staticmethod
    def validate_films(data: Dict[str, Any]) -> List[str]:
        """
        Validate data for films
        """
        errors = []

        try:
            if len(data.get("film_title", "")) > 100 or len(data.get("film_title", "")) < 3:
                errors.append("Length film title should be between 3 and 100 characters")
            if data.get("film_title", "").isdigit():
                errors.append("The film title should be string")
            default = datetime.strptime("1970-01-01", "%Y-%m-%d")

            if datetime.strptime(data.get("release_date", default), "%Y-%m-%d") \
                    < datetime.strptime("1971-01-01", "%Y-%m-%d"):
                errors.append("Release data should be more than 1971-01-01")

            if re.search("[A-Za-z]", str(data.get("rate", "F"))) or \
                    str(data.get("rate", "")).find(".") == -1:
                errors.append("The rate should be float")

            if data.get("rate", 0) < 0 or data.get("rate", 0) > 10:
                errors.append("Rate should be between 0 and 10")

            for item in data.get("genres"):
                nested_error = ValidateSchemas.validate_genre(item)
                if nested_error:
                    errors.extend(nested_error)

            for item in data.get("directors"):
                nested_error = ValidateSchemas.validate_director(item)
                if nested_error:
                    errors.extend(nested_error)
        except Exception as ex:
            logger.error(ex)
        return errors

    @classmethod
    def validate_user(cls, data: Dict[str, Any]) -> List[str]:
        """
        Validate data for user
        """
        errors = []

        try:
            if cls.validate_first_last_name_or_genre_length(data.get("first_name", "")):
                errors.append("Length first name should be between 3 and 100 characters")
            if cls.validate_first_last_name_or_genre_string(data.get("first_name", "")):
                errors.append("The first name should be string")

            if cls.validate_first_last_name_or_genre_length(data.get("last_name", "")):
                errors.append("Length last name should be between 3 and 100 characters")
            if cls.validate_first_last_name_or_genre_string(data.get("last_name", "")):
                errors.append("The last name should be string")

            if re.search("[A-Za-z]", str(data.get("age", ""))):
                errors.append("Age should be numeric")

            if data.get("age", 0) < 12:
                errors.append("The age should be more than 11")

            if str(data.get("age", "")).find(".") != -1:
                errors.append("The age should be numeric not float")

            regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
            if not re.fullmatch(regex, data.get("email", "")):
                errors.append("Invalid email")
            password = data.get("password", "")
            if len(password) < 8 or re.search("[0-9]", password) is None or \
                    re.search("[A-Z]", password) is None:
                errors.append("Make sure your password is at lest 8 letters,"
                              " has a number in it, has a capital letter in it")

        except Exception as ex:
            logger.error(ex)
        return errors
