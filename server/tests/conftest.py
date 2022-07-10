from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from flask import Flask

from flask_server.app import app as flask_app, db as app_db, encryption_handler
from flask_server.models import User
from pathlib import Path

import pytest


IMAGE_FILE_PARENT_DIRECTORY = Path(f"{__file__}/../../flask_server").resolve()


def clear_images():
    clothing_images = IMAGE_FILE_PARENT_DIRECTORY.joinpath(Path("./clothing_images")).resolve()
    post_images = IMAGE_FILE_PARENT_DIRECTORY.joinpath(Path("./post_images")).resolve()

    for file in clothing_images.iterdir():
        if file.name != "test.png":
            file.unlink()

    for file in post_images.iterdir():
        if file.name != "test.png":
            file.unlink()


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
        clear_images()
        app_db.drop_all()
