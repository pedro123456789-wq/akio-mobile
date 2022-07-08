from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from flask.testing import FlaskClient

from flask_server.app import db as app_db, encryption_handler
from flask_server.models import User


def test_profile(client: "FlaskClient"):
    new_user = User(
        username="test",
        hashed_password=encryption_handler.generate_password_hash("hash").decode()
    )
    app_db.session.add(new_user)

    response = client.get(f'/api/user/profile?username={new_user.username}')
    assert response.status_code == 200

    data = response.json.get('data')
    assert data is not None
    print(data)
    assert data.get('username') == new_user.username


def test_api(client: "FlaskClient"):
    # print(request)
    print(User.query.filter_by(username="test").first())
    response = client.get("/api")
    assert response.status_code == 200
    assert response.text == "api running..."
