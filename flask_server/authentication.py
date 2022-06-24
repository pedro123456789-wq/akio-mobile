from functools import wraps
import jwt
from datetime import datetime
from jsonschema import validate, exceptions


from flask_server.validation_schemes import sessionValidationSchema
from flask_server.models import User
from flask import request



def loginRequired(methods = None):
    if methods == None: 
        methods = ['GET', 'PUT', 'POST']

    def wrapper(function):
        @wraps(function)
        def decorated(*args, **kwargs):
            if request.method in methods:
                # for get requests data will be sent in headers
                if request.method == 'GET':
                    data = request.headers
                else:
                    data = request.get_json()

                #check if headers are valid with json schema
                try:
                    validate(data, schema = sessionValidationSchema)
                except exceptions.ValidationError as error:
                    return customResponse(False, error.message)

                username, token = data.get('username'), data.get('token')

                #check if token is valid and has not expired
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




