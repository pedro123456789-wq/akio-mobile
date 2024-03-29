from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flask.testing import FlaskClient

from flask_server.models import User, ClothingVariant, Size, Colour, ClothingItem
from conftest import make_test_user, make_test_clothing_item, make_test_clothing_variant, make_test_passworded_user, login

# Aim for 100% code coverage


# Todo: Test post count
def test_profile(client: "FlaskClient"):
    new_user = make_test_user()

    get_response = client.get(f'/api/user/profile?username={new_user.username}')
    assert get_response.status_code == 200
    assert get_response.json.get('message') == "Got profile data successfully"
    data = get_response.json.get('data')
    assert data is not None
    assert data == {'username': new_user.username, 'background_colour': None, 'clothing_id': None, 'image_url': None, 'posts': 0, 'likes': 0}

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


# @Pedro, this code is awful we need a better way of doing these assertions
# - Taran 12/7/22
# I think we could make a function that "dictionarifies" model objects,
# In the same way as the server does when returning them.
# So, we could compare the returned dictionary with the dictionarified one and they should be equal.
# This code could be written in util.py, and shared between the test code and the actual code for ease of use

def test_user_clothing_items(client: "FlaskClient"):
    url = "/api/user/clothing-items"

    user, pw = make_test_passworded_user()
    user2, pw2 = make_test_passworded_user()
    variant = make_test_clothing_variant()
    variant2 = make_test_clothing_variant()
    item = make_test_clothing_item(variant, user)
    item2 = make_test_clothing_item(variant2, user2)

    token = login(user.username, pw, client)

    response = client.get(f"{url}?username={user.username}&token={token}")
    data = response.json.get("data")
    
    assert response.status_code == 200
    assert data is not None
    assert len(data) == 1
    response_item = data[0]
    assert response_item["uuid"] == item.uuid
    assert response_item["name"] == item.variant.name
    assert response_item["size"] == item.variant.size.size
    assert response_item["colour"] == item.variant.colour.colour
    assert response_item["image_data"] == f"clothing_images/{response_item['uuid']}"

    token = login(user2.username, pw2, client)

    response = client.get(f"{url}?username={user2.username}&token={token}")
    data = response.json.get("data")

    assert response.status_code == 200
    assert data is not None
    assert len(data) == 1
    response_item = data[0]
    assert response_item["uuid"] == item2.uuid
    assert response_item["name"] == item2.variant.name
    assert response_item["size"] == item2.variant.size.size
    assert response_item["colour"] == item2.variant.colour.colour
    assert response_item["image_data"] == f"clothing_images/{response_item['uuid']}"


    bad_response = client.get(f"{url}?username=THISNAMEDOESNOTEXIST&token={token}")
    assert bad_response.status_code == 404


    # Possibly extract this test into a class, and test the get and post separately
    user, pw = make_test_passworded_user()
    item = make_test_clothing_item(variant)

    token = login(user.username, pw, client)

    response = client.post(url, json={
        "uuid": item.uuid,
        "username": user.username,
        "token": token
    })

    assert response.status_code == 200
    assert response.json.get("message") == "Added item to your collections"
    assert len(user.owned_clothes) == 1
    assert user.owned_clothes[0] == item

    
    bad_response = client.post(url, json={
        "uuid": "SAIUFGIUSAFHBSA",
        "username": user.username,
        "token": token
    })

    assert bad_response.status_code == 404
    assert bad_response.json.get("message") == "No clothing item found for that uuid"

    bad_response = client.post(url, json={
        "uuid": item.uuid,
        "username": "dshdshfsoidfiufoids",
        "token": token
    })

    assert bad_response.status_code == 404
    



def test_home(client: "FlaskClient"):
    # Test to make sure that database changes are not being rolled over between tests
    assert User.query.filter_by(username="test").first() is None

    response = client.get("/api")
    assert response.status_code == 200
    assert response.text == "api running..."
