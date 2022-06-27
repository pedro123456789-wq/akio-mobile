from datetime import datetime, timedelta
from pydantic import ValidationError
from jwt import encode

from flask import request
from flask_server import app, db
from flask_server import encryptionHandler
from flask_server import validation_schemas
from flask_server.authentication import loginRequired, adminRequired
from flask_server.models import User
from flask_server.responses import customResponse



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
    
    
@app.route('/api/clothing-items', methods = ['GET', 'POST', 'PUT'])
@loginRequired()
@adminRequired()
def clothingItems():
    if request.method == 'GET':
        pass

    elif request.method == 'POST':
        pass 
    
    elif request.method == 'PUT':
        pass 
    
    return 'Clothing items endpoint'
    # Admikn endpoint 
    # GET -> Return clothing variants already created
    # POST -> Create new clothing variant
    # PUT -> Edit or delete clothing variant 
    
    
@app.route('/api/user/profile', methods = ['GET', 'POST', 'PUT'])
def userProfile():
    # GET -> return user's icon colour and clothing item 
    # POST -> set user's icon colour and clothing item for the first time 
    # PUT -> change user's icon colour and clothing item
    
    pass 

@app.route('/api/user/clothing-items', methods = ['GET', 'POST', 'PUT'])
@loginRequired()
def userClothes():
    pass 


@app.route('/api/user/posts', methods = ['GET', 'POST', 'PUT'])
@loginRequired()
def userPosts():
    pass 
    
    
@app.route('/api/random-posts', methods = ['GET'])
@loginRequired(methods = ['GET'])
def getRandomPosts():
    # Get random posts to display in the photo feed
    pass 
    

    

