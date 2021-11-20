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
    FORMAT = '%(asctime)s - %(name)s:%(lineno)s - %(levelname)s ' \
             '- FUNCTION=%(funcName)s - %(message)s'
    logger.setLevel(logging.INFO)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(FORMAT, datefmt='%d-%m-%Y %H:%M:%S'))
    sh.setLevel(logging.INFO)
    fh = logging.handlers.RotatingFileHandler(filename=os.getcwd() + '/movies/logs/movies.log',
                                              maxBytes=10*ONE_MB, backupCount=100)
    fh.setFormatter(logging.Formatter(FORMAT, datefmt='%d-%m-%Y %H:%M:%S'))
    fh.setLevel(logging.INFO)
    logger.addHandler(sh)
    logger.addHandler(fh)


class Configuration:
    """
    Configuration for application
    """

    SECRET_KEY = 'secret'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1@localhost:5432/dbname'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///movies.db'
    SQLALCHEMY_ECHO = True


class TestConfiguration(Configuration):
    """
    Configuration for tests
    """

    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:testing.db'
