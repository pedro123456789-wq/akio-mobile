from flask import request
from pydantic import ValidationError

from flask_server import validation_schemas
from flask_server.responses import custom_response


def extract_login_data():
    data = request.get_json()

    try:
        validation_schemas.SignUp(**data)
    except ValidationError as error:
        top_error = error.errors()[0]
        error_string = f"{top_error['msg']} for {top_error['loc'][0]}"
        return custom_response(False, error_string)

    username, password = data.get("username"), data.get("password")

    return username, password


def extract_data():
    if request.method in ["POST", "PUT", "DELETE"]:
        data = request.get_json()
    elif request.method == 'GET':
        data = request.args
    else:
        raise Exception("Invalid HTTP method passed to extract data!")

    return data
