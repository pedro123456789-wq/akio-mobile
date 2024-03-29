from functools import wraps
import jwt
from datetime import datetime
from pydantic import ValidationError
from flask import request

from flask_server.app import app
from flask_server.responses import custom_response
from flask_server.validation_schemas import SessionValidation
from flask_server.models import User
from flask_server.util import extract_data


# Todo: use utility function data extraction
# Need to pass token as a AUTHORISATION BEARER HEADER instead of in URL for security
# ^ Because currently we cant read it when its sent as part of a get request

def login_required(methods=None):
    if methods is None:
        methods = ["GET", "PUT", "POST"]

    def wrapper(function):
        @wraps(function)
        def decorated(*args, **kwargs):
            if request.method in methods:
                # for GET requests data will be sent in headers but for POST and PUT requests it will be sent as json in request body

                data = extract_data()
                    
                # check if headers are valid with json schema
                try:
                    SessionValidation(**data)
                except ValidationError as error:
                    top_error = error.errors()[0]
                    error_string = f"{top_error['msg']} for {top_error['loc'][0]}"
                    return custom_response(False, error_string)


                username, token = data.get("username"), data.get("token")
                
                # print(token)

                # check if token is valid and has not expired
                try:
                    decoded_token = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
                    token_username, token_expiration = decoded_token.get("username"), decoded_token.get("exp")

                    if token_username != username:
                        return custom_response(False, "Token does not match username")
                    elif datetime.fromtimestamp(token_expiration) < datetime.now():
                        return custom_response(False, "Token has expired")
                except Exception as e:
                    print(e)
                    return custom_response(False, "Invalid token")

            return function(*args, **kwargs)
        return decorated
    return wrapper


def admin_required(methods=None):
    if methods is None:
        methods = ["GET", "POST", "PUT"]

    def wrapper(function):
        @wraps(function)
        def decorated(*args, **kwargs):
            if request.method in methods:
                data = extract_data()

                username = data.get('username')
                if username:
                    target_user = User.query.filter_by(username=username).first()
                    
                    if not target_user.is_admin:
                        return custom_response(False, 'The given user is not an admin')
                else:
                    return custom_response(False, 'You did not send a username')

                return function(*args, **kwargs)
        return decorated
    return wrapper
