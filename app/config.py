from os.path import dirname, join
import os

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '57e19ea558d4967a552d03deece34a70'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SESSION_TYPE = "filesystem"
    SESSION_FILE_DIR = join(dirname(__file__), "../cache")


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class DevelopmentConfig(Config):
    ENV = "development"
    DEVELOPMENT = True
    DEBUG = True
    XERO_CLIENT_ID = u"9DE807BFD2C44724B9C4E0CA5CED7B64"
    XERO_CLIENT_SECRET = u"KeqQAs4qTMXeB7rpg5fxkRSmDJ97KZ0bDe6zFhoQIAWVA4sG"
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://whatsleft:whatsleft@db-postgres/usable_balance'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

# configure file based session

config = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig,
    'default': DevelopmentConfig,
}