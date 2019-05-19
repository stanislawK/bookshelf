from flask import Flask

from bookshelf.extensions import db, migrate, sess
from bookshelf.blueprints import book_api, book_form, books_list


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
    sess.init_app(app)


def register_blueprints(app):
    app.register_blueprint(book_api.book_api)
    app.register_blueprint(book_form.book_blueprint)
    app.register_blueprint(books_list.books_blueprint)
