import os

from flask import current_app
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ["SECRET_KEY"]
    POSTGRES_USER = os.environ["POSTGRES_USER"]
    POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
    POSTGRES_HOSTNAME = os.environ["POSTGRES_HOSTNAME"]
    POSTGRES_PORT = os.environ["POSTGRES_PORT"]
    POSTGRES_DB = os.environ["POSTGRES_DB"]
    APPLICATION_DB = os.environ["APPLICATION_DB"]
    JWT_HASH_METHOD = os.environ["JWT_HASH_METHOD"]
    JWT_EXP_TIME_DAYS = os.environ["JWT_EXP_TIME_DAYS"]
    MEDIA_PATH = os.environ["MEDIA_PATH"]


class ProductionConfig(Config):
    """ Production configurations """


class DevelopmentConfig(Config):
    """ Development configurations """
    TESTING = False
    ENV = os.environ["FLASK_CONFIG"]
    DEBUG = True

class TestingConfig(Config):
    """ Testing configurations """
    TESTING = True
    ENV = os.environ["FLASK_CONFIG"]
    DEBUG = True
