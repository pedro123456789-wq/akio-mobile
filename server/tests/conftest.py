from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from flask import Flask
    from flask.testing import FlaskClient

from flask_server.app import app as flask_app, db as app_db, encryption_handler
from flask_server.models import User, ClothingVariant, ClothingItem, Size, Colour
from pathlib import Path
from uuid import uuid4 as uuid
from random import choice

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


def make_test_passworded_user():
    password = uuid().hex
    new_user = User(
        username=uuid().hex[:8],
        hashed_password=encryption_handler.generate_password_hash(password).decode()
    )
    app_db.session.add(new_user)
    return new_user, password


def make_test_user():
    user, pw = make_test_passworded_user()
    return user


def make_test_clothing_variant():
    sizes = ["Small", "Medium", "Large"]
    colours = ["Red", "Green", "Blue"]

    rand_size = choice(sizes)
    rand_colour = choice(colours)
    size = Size.query.filter_by(size=rand_size).first() or Size(size=rand_size)
    colour = Colour.query.filter_by(colour=rand_colour).first() or Colour(colour=rand_colour)

    new_clothing = ClothingVariant(
        uuid=uuid().hex,
        name="A test hoodie",
        size=size,
        colour=colour
    )

    with open(IMAGE_FILE_PARENT_DIRECTORY.joinpath(Path(f"./clothing_images/test.png")).resolve(), "rb") as original_file:
        with open(IMAGE_FILE_PARENT_DIRECTORY.joinpath(Path(f"./clothing_images/{new_clothing.uuid}")).resolve(), "wb") as new_file:
            new_file.write(original_file.read())

    app_db.session.add(new_clothing)
    return new_clothing


def make_test_clothing_item(variant: ClothingVariant, user=None):
    clothing_item = ClothingItem(
        variant=variant,
        uuid=uuid().hex,
        user=user
    )

    app_db.session.add(clothing_item)
    return clothing_item


def login(user: str, pw: str, client: "FlaskClient") -> str:
    response = client.post("/api/login", json={
        'username': user,
        'password': pw
    })

    assert response.status_code == 200
    token = response.json.get("token")
    assert token is not None
    return token


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
