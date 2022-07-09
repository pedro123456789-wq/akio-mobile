import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flask.testing import FlaskClient

from flask_server.app import db as app_db, encryption_handler
from flask_server.models import User, ClothingVariant, Size, Colour
from pathlib import Path


# Aim for 100% code coverage


def make_test_user():
    new_user = User(
        username="test",
        hashed_password=encryption_handler.generate_password_hash("test_password").decode()
    )
    app_db.session.add(new_user)
    return new_user


def make_test_clothing_variant():
    new_clothing = ClothingVariant(
        uuid="1114cfe8e05a4f89b77f371816b28553",
        name="A test hoodie",
        size=(Size(size="Medium")),
        colour=(Colour(colour="Blue"))
    )

    with open(Path(f"../flask_server/clothing_images/test.png").resolve(), "rb") as original_file:
        with open(Path(f"../flask_server/clothing_images/{new_clothing.uuid}").resolve(), "wb") as new_file:
            new_file.write(original_file.read())

    app_db.session.add(new_clothing)
    return new_clothing


def test_profile(client: "FlaskClient"):
    new_user = make_test_user()

    get_response = client.get(f'/api/user/profile?username={new_user.username}')
    assert get_response.status_code == 200
    assert get_response.json.get('message') == "Got profile data successfully"
    data = get_response.json.get('data')
    assert data is not None
    assert data == {'username': new_user.username, 'background_colour': None, 'clothing_id': None, 'image_url': None}

    bad_response = client.get(f'/api/user/profile?username=doesnotexist')
    assert bad_response.status_code == 404
    assert bad_response.json.get('message') == "User not found"

    new_clothing = make_test_clothing_variant()
    put_response = client.put('/api/user/profile',
                              json={"background_colour": "#123456", "clothing_id": new_clothing.uuid,
                                    "username": new_user.username})

    assert put_response.status_code == 200
    assert put_response.json.get('message') == "Updated profile successfully"
    assert new_user.background_colour == "#123456"
    assert new_user.clothing_id == new_clothing.uuid

    bad_hex = client.put("/api/user/profile",
                         json={"background_colour": "hahaha", "clothing_id": new_clothing.uuid,
                               "username": new_user.username})
    assert bad_hex.status_code == 400
    assert bad_hex.json.get('message') == "Invalid hex value for background_colour"

    bad_uuid = client.put("/api/user/profile",
                          json={"background_colour": "#324122", "clothing_id": "i dont exist",
                                "username": new_user.username})
    assert bad_uuid.status_code == 400
    assert bad_uuid.json.get('message') == "Invalid uuid entered for clothing_id"


def test_clothing_items():
    user = make_test_user()
    variant = make_test_clothing_variant()


def test_home(client: "FlaskClient"):
    # Test to make sure that database changes are not being rolled over between tests
    assert User.query.filter_by(username="test").first() is None

    response = client.get("/api")
    assert response.status_code == 200
    assert response.text == "api running..."
