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


# Auto-run for every test
@pytest.fixture(autouse=True)
def db(app: "Flask"):
    with app.app_context():
        app_db.create_all()

        yield

        # Drop all changes (rolling back or closing does not work because the routes will call commit)
        app_db.drop_all()
