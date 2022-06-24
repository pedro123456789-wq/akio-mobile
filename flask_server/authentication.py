from functools import wraps
import jwt
from datetime import datetime
from pydantic import ValidationError

from flask_server import app
from flask_server.responses import customResponse
from flask_server.validation_schemas import SessionValidation
from flask_server.models import User
from flask import request


def loginRequired(methods=None):
    if methods == None:
        methods = ['GET', 'PUT', 'POST']

    def wrapper(function):
        @wraps(function)
        def decorated(*args, **kwargs):
            if request.method in methods:
                # for GET requests data will be sent in headers but for POST and PUT requests it will be sent as json in request body
                if request.method == 'GET':
                    data = request.headers
                else:
                    data = request.get_json()

                # check if headers are valid with json schema
                try:
                    SessionValidation(**data)
                except ValidationError as error:
                    topError = error[0]
                    errorString = f"{topError['message']} for {topError['loc']}"
                    return customResponse(False, errorString)

                username, token = data.get('username'), data.get('token')

                # check if token is valid and has not expired
                try:
                    decodedToken = jwt.decode(token, app.config['SECRET_KEY'])
                    tokenUsername, tokenExpiration = decodedToken.get('user'), decodedToken.get('exp')

                    if tokenUsername != username:
                        return customResponse(False, 'Token does not match username')
                    elif datetime.fromtimestamp(tokenExpiration) < datetime.now():
                        return customResponse(False, 'Token has expired')
                except Exception:
                    return customResponse(False, 'Invalid token')

            return function(*args, **kwargs)
        return decorated
    return wrapper
