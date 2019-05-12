import os
import tempfile

import pytest

from bookshelf.app import create_app
from bookshelf.extensions import db


@pytest.fixture
def app():
    """Create and configure a new app instance for tests."""

    # create a temp file to isolate the db for each test
    db_fd, db_path = tempfile.mkstemp()
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DATABASE'] = db_path
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"

    # create db and load test data
    with app.app_context():
        db.init_app(app)
        db.create_all()

    yield app

    # close and remove the temporary db
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app"""
    return app.test_client()


@pytest.fixture
def _db():
    """Create and configure a new db instance"""
    db_fd, db_path = tempfile.mkstemp()
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DATABASE'] = db_path
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"

    with app.app_context():
        db.init_app(app)
        db.create_all()

        yield db

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def new_book():
    book = {'title': 'Hobbit',
            'description': 'Some book about little hobbits.'}
    return book


@pytest.fixture
def new_author():
    return {'name': 'J.R.R. Tolkien'}


@pytest.fixture
def new_category():
    return {'name': 'Juvenile Fiction'}
