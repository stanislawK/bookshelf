import os


class Config(object):
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://{username}:{password}@{hostname}:{port}/{dbname}"
        .format(
            username=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            hostname=os.environ.get("DB_HOST"),
            port=os.environ.get("PORT"),
            dbname=os.environ.get("DB_NAME")
        )
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('TRACK')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SESSION_TYPE = 'filesystem'


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True

    SQLALCHEMY_DATABASE_URI = (
        "postgresql:///bookshelf"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'Secret123'
    SESSION_TYPE = 'filesystem'
