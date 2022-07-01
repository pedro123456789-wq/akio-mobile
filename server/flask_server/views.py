from datetime import datetime, timedelta
from logging.config import valid_ident
from pydantic import ValidationError
from jwt import encode

from flask import request
from flask_server import app, db
from flask_server import encryption_handler
from flask_server import validation_schemas
from flask_server.authentication import login_required, admin_required
from flask_server.models import ClothingItem, ClothingVariant, User, Colour, Size
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
        top_error = error.errors()[0]
        error_string = f"{top_error['msg']} for {top_error['loc']}"
        return custom_response(False, error_string)

    username, password = data.get("username"), data.get("password")
    hashed_password = encryption_handler.generate_password_hash(
        password).decode("utf-8")

    # check if username is already in use
    matching_usernames = User.query.filter_by(username=username).all()
    if len(matching_usernames) > 0:
        return custom_response(False, "The username is already taken")

    # if username is admin and password is equal to secret key create admin account
    # checking if the password is equal to secret key ensures that normal users cannot create admin accounts

    if username == 'admin' and password == app.config['SECRET_KEY']:
        new_user = User(username=username,
                        hashed_password=hashed_password, is_admin=True)
    else:
        new_user = User(username=username,
                        hashed_password=hashed_password, is_admin=False)

    db.session.add(new_user)
    db.session.commit()

    return custom_response(True, "New account created")


# TODO: Test endpoint
@app.route("/api/login", methods=["POST"])
def login():
    """Api endpoint to create authenticated user session through jwt token"""
    data = request.get_json()

    try:
        validation_schemas.SignUp(**data)
    except ValidationError as error:
        top_error = error.errors()[0]
        error_string = f"{top_error['msg']} for {top_error['loc']}"
        return custom_response(False, error_string)

    username, password = data.get("username"), data.get("password")
    target_user = User.query.filter_by(username=username).first()

    if target_user:
        target_password = target_user.hashed_password

        if encryption_handler.check_password_hash(target_password, password):
            token = encode({"username": username, "exp": datetime.utcnow(
            ) + timedelta(hours=6)}, app.config["SECRET_KEY"]).decode()
            return custom_response(True, "Login Completed", token=str(token))
        else:
            return custom_response(False, "Incorrect password")
    else:
        return custom_response(False, "Account does not exist")


@app.route("/api/clothing-variants", methods=["GET", "POST", "PUT"])
@login_required()
@admin_required()
def clothing_items():
    if request.method == 'POST' or request.method == 'PUT':
        data = request.get_json()
    elif request.method == 'GET':
        data = request.headers
        data = {k.lower(): v for k, v in data.items()}

    
    if request.method == "GET":
        variants = ClothingVariant.query.all()
        output = [{
            'uuid': variant.uuid,
            'name': variant.name,
            'size':  Size.query.filter_by(id = variant.size_id).first().size,
            'colour': Colour.query.filter_by(id = variant.colour_id).first().colour
        } for variant in variants]

        return custom_response(True, 'Fetched data successfully', data=output)

    elif request.method == "POST":
        # add clothing variants to database
        try:
            validation_schemas.ClothingVariant(**data)
        except ValidationError as error:
            top_error = error.errors()[0]
            error_string = f"{top_error['msg']} for {top_error['loc']}"
            return custom_response(False, error_string)

        uuid, name, colour, size = data.get('uuid'), data.get('name'), data.get('colour'), data.get('size')
        targetColour = Colour.query.filter_by(colour=colour).first()
        targetSize = Size.query.filter_by(size=size).first()

        # if chosen colour is not in database add it to database
        if not targetColour:
            targetColour = Colour(colour=colour)
            db.session.add(targetColour)
            db.session.flush()

        # if chosen size is not in database add it to database
        if not targetSize:
            targetSize = Size(size=size)
            db.session.add(targetSize)
            db.session.flush()

        # add new clothing variant
        newVariant = ClothingVariant(
            uuid=uuid, name=name, colour_id=targetColour.id, size_id=targetSize.id)
        db.session.add(newVariant)
        db.session.commit()

        return custom_response(True, 'Added item to database')

    elif request.method == "PUT":
        # delete clothing variant
        uuid = data.get('uuid')
        if not uuid or type(uuid) != int:
            return custom_response(False, 'Invalid uuid')

        targetVariant = ClothingVariant.query.filter_by(uuid=uuid).first()
        if targetVariant:
            db.session.delete(targetVariant)
            db.session.commit()

            return custom_response(True, 'Deleted item successfully')
        else:
            return custom_response(False, 'No items match given uuid')


@app.route("/api/user/profile", methods=["GET", "POST", "PUT"])
def user_profile():
    # GET -> return user"s icon colour and clothing item
    # POST -> set user"s icon colour and clothing item for the first time
    # PUT -> change user"s icon colour and clothing item

    pass


@app.route("/api/user/clothing-items", methods=["GET", "POST", "PUT"])
@login_required()
def user_clothes():
    if request.method == 'POST' or request.method == 'PUT':
        data = request.get_json()
    elif request.method == 'GET':
        data = request.headers
        data = {k.lower(): v for k, v in data.items()}

    if request.method == 'GET':
        pass

    if request.method == 'POST':
        # allow user to add item to their collection by scanning it
        uuid = data.get('uuid')

        if not uuid or type(uuid) != int:
            return custom_response(False, 'You did not provide a valid uuid')

        targetUser = User.query.filter_by(
            username=data.get('username')).first()
        targetItem = ClothingVariant.query.filter_by(uuid=uuid).first()

        if targetItem:
            targetUser.owned_clothes.append(targetItem)
            # also return information about the item
            db.session.commit()

            return custom_response(True, 'Added item to your collections')
        else:
            return custom_response(False, 'No clothing item found for that uuid')

    elif request.method == 'PUT':
        pass


@app.route("/api/user/posts", methods=["GET", "POST", "PUT"])
@login_required()
def user_posts():
    pass


@app.route("/api/random-posts", methods=["GET"])
@login_required(methods=["GET"])
def get_random_posts():
    # Get random posts to display in the photo feed
    pass
