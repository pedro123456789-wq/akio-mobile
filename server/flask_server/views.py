from datetime import datetime, timedelta
from logging.config import valid_ident
from os import path, listdir
from pydantic import ValidationError
from jwt import encode
from random import choice
from string import ascii_lowercase, digits
import base64

from flask import request
from flask_server import app, db
from flask_server import encryption_handler
from flask_server import validation_schemas
from flask_server.authentication import login_required, admin_required
from flask_server.models import ClothingItem, ClothingVariant, User, Colour, Size, Post
from flask_server.responses import custom_response


# TODO:
# Add better validation for scanning endpoint
# add images to posts and clothing variants


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
        error_string = f"{top_error['msg']} for {top_error['loc'][0]}"
        return custom_response(False, error_string)

    username, password = data.get("username"), data.get("password")
    hashed_password = encryption_handler.generate_password_hash(
        password).decode("utf-8")

    # check if username is already in use
    matching_usernames = User.query.filter_by(username=username).all()
    if len(matching_usernames) > 0:
        return custom_response(False, "The username is already taken")

    # generate random background colour and uuid for user profile
    random_hex = '#' + ''.join([choice(list(ascii_lowercase)[0: 6] + list(digits))
                                for _ in range(6)])  # pick 6 random letters (a - f) or numbers

    items = ClothingVariant.query.all()
    random_uuid = int(choice(items).uuid)

    # if username is 'admin' and password is equal to secret key create admin account
    # checking if the password is equal to secret key ensures that normal users cannot create admin accounts
    if username == 'admin' and password == app.config['SECRET_KEY']:
        new_user = User(username=username,
                        hashed_password=hashed_password,
                        background_colour=random_hex,
                        clothing_id=random_uuid,
                        is_admin=True)
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
    data = request.get_json()

    try:
        validation_schemas.SignUp(**data)
    except ValidationError as error:
        top_error = error.errors()[0]
        error_string = f"{top_error['msg']} for {top_error['loc'][0]}"
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

# allow user to send list of required uuids instead of sending whole collection of clothes 
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
        output = []

        for variant in variants:
            # get base64 for image
            if not path.isfile(f'./flask_server/clothing_images/{variant.uuid}.png'):
                base64_string = ''
            else:
                with open(f'./flask_server/clothing_images/{variant.uuid}.png', 'rb') as image_file:
                    base64_string = base64.b64encode(image_file.read())
                    image_file.close()
                
            output.append({
                'uuid': variant.uuid,
                'name': variant.name,
                'size':  Size.query.filter_by(id=variant.size_id).first().size,
                'colour': Colour.query.filter_by(id=variant.colour_id).first().colour,
                'image_data': base64_string
            })

        return custom_response(True, 'Fetched data successfully', data=output)

    elif request.method == "POST":
        # add clothing variants to database
        try:
            validation_schemas.ClothingVariantValidator(**data)
        except ValidationError as error:
            top_error = error.errors()[0]
            error_string = f"{top_error['msg']} for {top_error['loc'][0]}"
            return custom_response(False, error_string)

        uuid, name, colour, size, image_data = data.get('uuid'), data.get('name'), data.get('colour'), data.get('size'), data.get('image_data')
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

        # save image in clothing_images folder
        clothing_image = base64.b64decode(image_data)
        with open(f'./flask_server/clothing_images/{uuid}.png', 'wb') as image_file:
            image_file.write(clothing_image)
            image_file.close()

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

    if request.method == 'POST' or request.method == 'PUT':
        data = request.get_json()
    elif request.method == 'GET':
        data = request.headers
        data = {k.lower(): v for k, v in data.items()}

    target_user = User.query.filter_by(username=data.get('username')).first()

    if request.method == 'GET':
         # get base64 string for image
        if not path.isfile(f'./flask_server/clothing_images/{target_user.clothing_id}.png'):
            base64_string = ''
        else:
            with open(f'./flask_server/clothing_images/{target_user.clothing_id}.png', 'rb') as image_file:
                base64_string = base64.b64encode(image_file.read())
                image_file.close()
                
        output = {
            'username': data.get('username'),
            'background_colour': target_user.background_colour,  # hex value
            'clothing_id': target_user.clothing_id, 
            'image_data': base64_string
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
    if request.method == 'POST' or request.method == 'PUT':
        data = request.get_json()
    elif request.method == 'GET':
        data = request.headers
        data = {k.lower(): v for k, v in data.items()}

    if request.method == 'GET':
        targetUser = User.query.filter_by(
            username=data.get('username')).first()
        owned_clothes = targetUser.owned_clothes

        output = []
        for item in owned_clothes:
            item_data = ClothingVariant.query.filter_by(uuid=item.varient_id).first()
            
            # get base64 string for image
            if not path.isfile(f'./flask_server/clothing_images/{item_data.uuid}.png'):
                base64_string = ''
            else:
                with open(f'./flask_server/clothing_images/{item_data.uuid}.png', 'rb') as image_file:
                    base64_string = base64.b64encode(image_file.read())
                    image_file.close()
                    
            output.append({
                'uuid': item_data.uuid,
                'name': item_data.name,
                'size': Size.query.filter_by(id=item_data.size_id).first().size,
                'color': Colour.query.filter_by(id=item_data.colour_id).first().colour, 
                'image_data': base64_string
            })

        return custom_response(True, 'Fetched data successfully', data=output)

    if request.method == 'POST':
        # allow user to add item to their collection by scanning it
        uuid = data.get('uuid')

        if not uuid or type(uuid) != int:
            return custom_response(False, 'You did not provide a valid uuid')

        targetUser = User.query.filter_by(username=data.get('username')).first()
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
    
    if request.method == 'POST' or request.method == 'PUT':
        data = request.get_json()
    elif request.method == 'GET':
        data = request.headers
        data = {k.lower(): v for k, v in data.items()}
        
    target_user = User.query.filter_by(username = data.get('username')).first()

    if request.method == 'GET':
        # get all posts made by the user 
        pass 
    elif request.method == 'POST':
        try:
            validation_schemas.PostValidation(**data)
        except ValidationError as error:
            top_error = error.errors()[0]
            error_string = f"{top_error['msg']} for {top_error['loc'][0]}"
            return custom_response(False, error_string)
        
        caption, image_data = data.get('caption'), data.get('image_data')
        
        # generate unique id for post 
        uuid = len(listdir('./flask_server/post_images'))
        
        # add new post to database
        new_post = Post(caption = caption, uuid = uuid, poster_id = target_user.id)
        db.session.add(new_post)
        db.session.commit()
        
        # save image in post_images folder
        clothing_image = base64.b64decode(image_data)
        with open(f'./flask_server/post_images/{uuid}.png', 'wb') as image_file:
            image_file.write(clothing_image)
            image_file.close()
        
        
        return custom_response(True, 'Post made successfully')
    
        
    elif request.method == 'PUT':
        uuid = data.get('uuid')
        post = Post.query.filter_by(uuid = uuid).first()
        
        # check if post exists
        if post:
            # check if user owns the post it is trying to delete
            if post.poster_id == target_user.id:
                db.session.delete(post)
                db.session.commit()
                return custom_response(True, 'Post deleted successfully')
            else:
                return custom_response(False, 'You do not own this post')
        else:
            return custom_response(False, 'Post does not exist')
        


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
