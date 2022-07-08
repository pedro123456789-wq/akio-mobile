from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from flask.testing import FlaskClient

from flask import request


def test_api(client: "FlaskClient"):
    # print(request)
    response = client.get("/api")
    assert response.status_code == 200
    assert response.text == "api running..."
