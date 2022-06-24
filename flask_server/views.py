from datetime import datetime, timedelta
from pydantic import ValidationError
from jwt import encode

from flask import request
from flask_server import app, db
from flask_server import encryptionHandler
from flask_server import validation_schemas
from flask_server.models import User
from flask_server.responses import customResponse
from flask_server import validation_schemas


@app.route("/api")
def home():
    return "api running..."


# TODO: Test Endpoint
@app.route("/api/sign-up", methods=["POST"])
def signUp():
    """Api endpoint to create new user account"""
    data = request.get_json()

    try:
        validation_schemas.SignUp(**data)
    except ValidationError as error:
        topError = error[0]
        errorString = f"{topError['message']} for {topError['loc']}"
        return customResponse(False, errorString)

    username, password = data.get("username"), data.get("password")
    hashedPassword = encryptionHandler.generate_password_hash(password).decode("utf-8")

    # check if username is already in use
    matchingUsernames = User.query.filter_by(username=username).all()
    if len(matchingUsernames) > 0:
        return customResponse(False, "The username is already taken")

    newUser = User(username=username, passwordHash=hashedPassword)
    db.session.add(newUser)
    db.session.commit()

    return customResponse(True, "New account created")

# TODO: Test endpoint 
@app.route('/api/login', methods=['POST'])
def login():
    """Api endpoint to create authenticated user session through jwt token"""
    data = request.get_json()

    try:
        validation_schemas.SignUp(**data)
    except ValidationError as error:
        topError = error[0]
        errorString = f"{topError['message']} for {topError['loc']}"
        return customResponse(False, errorString)

    username, password = data.get('username'), data.get('password')
    targetUser = User.query.filter_by(username=username).first()

    if targetUser:
        targetPassword = targetUser.password

        if encryptionHandler.check_password_hash(targetPassword, password):
            token = encode({"username": username, "exp": datetime.utcnow() + timedelta(hours=6)}, app.config['SECRET_KEY']).decode("utf-8")
            return customResponse(True, "Login Completed", token=str(token))
        else:
            return customResponse(False, "Incorrect password")
    else:
        return customResponse(False, "Account does not exist")
