from jsonschema import validate, exceptions

from flask_server import app, db
from flask_server import encryptionHandler
from flask_server import validation_schemes
from flask_server.models import User


@app.route('/api')
def home():
    return 'api running...'


@app.route('/api/sign-up', methods = ['POST'])
def signUp():
    data = request.get_json()

    try:
        validate(data, schema=validation_schemes.signUpSchema)
    except exceptions.ValidationError as error:
        # TODO: Return error response
        return -1

    username, password = data.get('username'), data.get('password')
    hashedPassword = encryptionHandler.generate_password_hash(password).decode('utf-8')

    newUser = User(username = username, passwordHash = hashedPassword)




