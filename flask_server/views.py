from datetime import datetime, timedelta
from pydantic import ValidationError
from jwt import encode

from flask import request
from flask_server import app, db
from flask_server import migration_handler
from flask_server import validation_schemas
from flask_server.authentication import login_required, admin_required
from flask_server.models import User
from flask_server.responses import custom_response



@app.route("/api")
def home():
    return "api running..."


# TODO: Test Endpoint
@app.route("/api/sign-up", methods=["POST"])
def sign_up():
    """Api endpoint to create new user account"""
    data = request.get_json()

    try:
        validation_schemas.SignUp(**data)
    except ValidationError as error:
        top_error = error[0]
        error_string = f"{top_error['message']} for {top_error['loc']}"
        return custom_response(False, error_string)

    username, password = data.get("username"), data.get("password")
    hashed_password = migration_handler.generate_password_hash(password).decode("utf-8")

    # check if username is already in use
    matching_usernames = User.query.filter_by(username=username).all()
    if len(matching_usernames) > 0:
        return custom_response(False, "The username is already taken")

    new_user = User(username=username, passwordHash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return custom_response(True, "New account created")


# TODO: Test endpoint 
@app.route('/api/login', methods=['POST'])
def login():
    """Api endpoint to create authenticated user session through jwt token"""
    data = request.get_json()

    try:
        validation_schemas.SignUp(**data)
    except ValidationError as error:
        top_error = error[0]
        error_string = f"{top_error['message']} for {top_error['loc']}"
        return custom_response(False, error_string)

    username, password = data.get('username'), data.get('password')
    target_user = User.query.filter_by(username=username).first()

    if target_user:
        target_password = target_user.password

        if migration_handler.check_password_hash(target_password, password):
            token = encode({"username": username, "exp": datetime.utcnow() + timedelta(hours=6)}, app.config['SECRET_KEY']).decode("utf-8")
            return custom_response(True, "Login Completed", token=str(token))
        else:
            return custom_response(False, "Incorrect password")
    else:
        return custom_response(False, "Account does not exist")
    
    
@app.route('/api/clothing-items', methods = ['GET', 'POST', 'PUT'])
@login_required()
@admin_required()
def clothing_items():
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
def user_profile():
    # GET -> return user's icon colour and clothing item 
    # POST -> set user's icon colour and clothing item for the first time 
    # PUT -> change user's icon colour and clothing item
    
    pass 

@app.route('/api/user/clothing-items', methods = ['GET', 'POST', 'PUT'])
@login_required()
def user_clothes():
    pass 


@app.route('/api/user/posts', methods = ['GET', 'POST', 'PUT'])
@login_required()
def user_posts():
    pass 
    
    
@app.route('/api/random-posts', methods = ['GET'])
@login_required(methods = ['GET'])
def get_random_posts():
    # Get random posts to display in the photo feed
    pass 
    

    

