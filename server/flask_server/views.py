from datetime import datetime, timedelta
from logging.config import valid_ident
from pydantic import ValidationError
from jwt import encode
from random import choice
from string import ascii_lowercase, digits

from flask import request
from flask_server import app, db
from flask_server import encryption_handler
from flask_server import validation_schemas
from flask_server.authentication import login_required, admin_required
from flask_server.models import ClothingItem, ClothingVariant, User, Colour, Size
from flask_server.responses import custom_response
from .util import extract_login_data, extract_data


# TODO: 
# Add better validation for scanning endpoint
# add images to posts and clothing variants


@app.route("/api")
def home():
    return "api running..."


@app.route("/api/sign-up", methods=["POST"])
def sign_up():
    """Api endpoint to create new user account"""
    username, password = extract_login_data()

    hashed_password = encryption_handler.generate_password_hash(password).decode("utf-8")

    # check if username is already in use
    matching_usernames = User.query.filter_by(username=username).all()
    if len(matching_usernames) > 0:
        return custom_response(False, "The username is already taken")

    # generate random background colour and uuid for user profile
    random_hex = '#' + ''.join([choice(list(ascii_lowercase)[0: 6] + list(digits)) 
                                for _ in range(6)])  # pick 6 random letters (a - f) or numbers

    items = ClothingVariant.query.all()
    random_uuid = str(choice(items).uuid)

    # if username is 'admin' and password is equal to secret key create admin account
    # checking if the password is equal to secret key ensures that normal users cannot create admin accounts
    if username == 'admin':
        if password == app.config['SECRET_KEY']:
            new_user = User(username=username,
                            hashed_password=hashed_password,
                            background_colour=random_hex,
                            clothing_id=random_uuid,
                            is_admin=True)
        else:
            return custom_response(False, "Attempted to make admin account without the secret.")
    else:
        new_user = User(username=username,
                        hashed_password=hashed_password, 
                        background_colour=random_hex, 
                        clothing_id=random_uuid, 
                        is_admin=False)

    db.session.add(new_user)
    db.session.commit()

    return custom_response(True, "New account created")


@app.route("/api/login", methods=["POST"])
def login():
    """Api endpoint to create authenticated user session through jwt token"""
    username, password = extract_login_data()

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
    data = extract_data()

    if request.method == "GET":
        variants = ClothingVariant.query.all()
        output = [{
            'uuid': variant.uuid,
            'name': variant.name,
            'size':  Size.query.filter_by(id=variant.size_id).first().size,
            'colour': Colour.query.filter_by(id=variant.colour_id).first().colour
        } for variant in variants]

        return custom_response(True, 'Fetched data successfully', data=output)

    elif request.method == "POST":
        # add clothing variants to database
        try:
            validation_schemas.ClothingVariantValidator(**data)
        except ValidationError as error:
            top_error = error.errors()[0]
            error_string = f"{top_error['msg']} for {top_error['loc'][0]}"
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
    # GET -> return user's icon colour and clothing item
    # PUT -> change user's icon colour and clothing item uuid

    data = extract_data()

    target_user = User.query.filter_by(username=data.get('username')).first()

    if request.method == 'GET':
        output = {
            'username': data.get('username'),
            'background_colour': target_user.background_colour,  # hex value
            'clothing_id': target_user.clothing_id
        }

        return custom_response(True, 'Got profile data successfully', data=output)

    elif request.method == 'PUT':
        try:
            validation_schemas.ProfileData(**data)
        except ValidationError as error:
            top_error = error.errors()[0]
            error_string = f"{top_error['msg']} for {top_error['loc'][0]}"
            return custom_response(False, error_string)

        target_user.background_colour = data.get('background_colour')
        target_user.clothing_id = data.get('clothing_uuid')
        db.session.commit()

        return custom_response(True, 'Updated profile successfully')


@app.route("/api/user/clothing-items", methods=["GET", "POST"])
@login_required()
def user_clothes():
    data = extract_data()

    if request.method == 'GET':
        targetUser = User.query.filter_by(
            username=data.get('username')).first()
        owned_clothes = targetUser.owned_clothes

        output = []
        for item in owned_clothes:
            item_data = ClothingVariant.query.filter_by(
                uuid=item.varient_id).first()
            output.append({
                'uuid': item_data.uuid,
                'name': item_data.name,
                'size': Size.query.filter_by(id=item_data.size_id).first().size,
                'color': Colour.query.filter_by(id=item_data.colour_id).first().colour
            })

        return custom_response(True, 'Fetched data successfully', data=output)

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


@app.route("/api/user/posts", methods=["GET", "POST", "PUT"])
@login_required()
def user_posts():
    # GET -> See posts made by user
    # POST -> Publish new post
    # PUT -> delete post
    
    if request.method == 'GET':
        pass

    elif request.method == 'POST':
        pass 
    
    elif request.method == 'PUT':
        pass 



@app.route("/api/posts", methods=["GET"])
@login_required(methods=["GET"])
def get_random_posts():
    # GET -> Get random posts for the user
    # POST -> Actions: 
    #           Like: add like to post
    # PUT -> reomove post (admin endpoint) 
    
    
    if request.method == 'GET':
        pass 
    elif request.method == 'POST':
        pass 
    elif request.method == 'PUT':
        pass 
