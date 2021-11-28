# -*- coding: utf-8 -*-
"""
   Collect all configuration for project
"""

import logging
import logging.handlers
import os

ONE_MB = 1_000_000


def init_logger(name):
    """
    Init logger for application. Set formats for writing information to the files and
    for output to debug.
    """
    logger = logging.getLogger(name)
    logger_format = "%(asctime)s - %(name)s:%(lineno)s - %(levelname)s - " \
                    "FUNCTION=%(funcName)s - %(message)s"
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter(logger_format, datefmt='%d-%m-%Y %H:%M:%S'))
    stream_handler.setLevel(logging.INFO)
    file_handler = logging.handlers.RotatingFileHandler(filename=
                                                        os.getcwd() + "/movies/logs/movies.log",
                                                        maxBytes=10*ONE_MB, backupCount=100)
    file_handler.setFormatter(logging.Formatter(logger_format, datefmt="%d-%m-%Y %H:%M:%S"))
    file_handler.setLevel(logging.INFO)
    logger.addHandler(stream_handler)
    logger.addHandler(stream_handler)


class Configuration:
    """
    Configuration for application
    """

    SECRET_KEY = os.getenv("SECRET_KEY", "secret")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL",
                                        "postgresql://postgres:postgres_password@localhost:5433/movies")


class TestConfiguration(Configuration):
    """
    Configuration for tests
    """

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres_password@test_db:5434/test_movies"

