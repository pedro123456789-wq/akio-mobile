from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from flask import Flask

from flask_server.app import app as flask_app, db as app_db, encryption_handler
from flask_server.models import User

import pytest


@pytest.fixture()
def app():
    # Use in-memory sqlite database
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    flask_app.config["TESTING"] = True
    flask_app.testing = True

    yield flask_app


@pytest.fixture
def client(app: "Flask"):
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client


@pytest.fixture
def db(app: "Flask"):
    with app.app_context():
        app_db.session.add(User(
            username="test",
            hashed_password=encryption_handler.generate_password_hash("hash").decode()
        ))

        yield

        app_db.session.close()
