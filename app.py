from flask import Flask

from bookshelf.extensions import db, migrate
from bookshelf.blueprints import books


def create_app():
    """Application factiory function"""
    app = Flask(__name__)
    app.config.from_object('bookshelf.config.DevelopmentConfig')

    initialize_extensions(app)
    register_blueprints(app)

    return app


def initialize_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app):
    app.register_blueprint(books.books_blueprint)
