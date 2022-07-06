from datetime import datetime, timedelta
from os import path, listdir
from pydantic import ValidationError
from jwt import encode
from random import choice, sample
from string import ascii_lowercase, digits
from uuid import uuid4 as new_uuid
import base64

from flask import request, send_file
from flask_server import app, db
from flask_server import encryption_handler
from flask_server import validation_schemas
from flask_server.authentication import login_required, admin_required
from flask_server.models import ClothingItem, ClothingVariant, User, Colour, Size, Post, Like
from flask_server.responses import custom_response
from .util import extract_login_data, extract_data


# TODO:
# Add better validation for scanning endpoint
# Create tests
# Implement unlike functionality
# https://flask.palletsprojects.com/en/2.0.x/testing/


@app.route("/api")
def home():
    return "api running..."


@app.route("/api/sign-up", methods=["POST"])
def sign_up():
    """Api endpoint to create new user account"""
    username, password = extract_login_data()

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

# allow user to send list of required uuids instead of sending whole collection of clothes


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
            'colour': Colour.query.filter_by(id=variant.colour_id).first().colour,
            'image_url': f'clothing_images/{variant.uuid}'
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

        uuid = new_uuid().hex

        name, colour, size, image_data = data.get('name'), data.get('colour'), data.get('size'), data.get('image_data')
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

    data = extract_data()
    target_user = User.query.filter_by(username=data.get('username')).first()

    if request.method == 'GET':
        output = {
            'username': data.get('username'),
            'background_colour': target_user.background_colour,  # hex value
            'clothing_id': target_user.clothing_id,
            'image_url': f'clothing_images/{target_user.clothing_id}'
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
        target_user = User.query.filter_by(username=data.get('username')).first()
        owned_clothes = target_user.owned_clothes

        output = [{
                    'uuid': item.uuid,
                    'name': item.name,
                    'size': Size.query.filter_by(id=item.size_id).first().size,
                    'colour': Colour.query.filter_by(id=item.colour_id).first().colour,
                    'image_data': f'clothing_images/{item.uuid}'
        } for item in owned_clothes]

        return custom_response(True, 'Fetched data successfully', data=output)

    if request.method == 'POST':
        # allow user to add item to their collection by scanning it
        uuid = data.get('uuid')

        if not uuid:  # Don't need to make sure it's valid, an invalid uuid just won't return any results.
            return custom_response(False, 'You did not provide a uuid')

        target_user = User.query.filter_by(username=data.get('username')).first()
        target_item = ClothingVariant.query.filter_by(uuid=uuid).first()

        if target_item:
            target_user.owned_clothes.append(target_item)
            db.session.commit()

            return custom_response(True, 'Added item to your collections')
        else:
            return custom_response(False, 'No clothing item found for that uuid')


# TODO: Test endpoint
@app.route("/api/user/posts", methods=["GET", "POST", "PUT"])
@login_required()
def user_posts():
    # GET -> See posts made by user
    # POST -> Publish new post
    # PUT -> delete post
    data = extract_data()
    target_user = User.query.filter_by(username=data.get('username')).first()


    if request.method == 'GET':
        output = [{
            'id': post.id,
            'date_posted': post.date_posted,
            'caption': post.caption,
            'likes': len(post.liked_by),
            'image_url': f'/post_images/{post.id}'
        } for post in target_user.posts_made]

        return custom_response(True, 'Fetched data successfully', data=output)

    elif request.method == 'POST':
        try:
            validation_schemas.PostValidation(**data)
        except ValidationError as error:
            top_error = error.errors()[0]
            error_string = f"{top_error['msg']} for {top_error['loc'][0]}"
            return custom_response(False, error_string)

        caption, image_data = data.get('caption'), data.get('image_data')

        # generate unique id for post
        uuid = new_uuid().hex

        # add new post to database
        new_post = Post(caption=caption, uuid=uuid, poster_id=target_user.id)
        db.session.add(new_post)
        db.session.commit()

        # save image in post_images folder
        clothing_image = base64.b64decode(image_data)
        with open(f'./flask_server/post_images/{uuid}.png', 'wb') as image_file:
            image_file.write(clothing_image)
            image_file.close()

        return custom_response(True, 'Post made successfully')

    elif request.method == 'PUT':
        post_id = data.get('id')
        post = Post.query.filter_by(id=post_id).first()

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
    #           Unlike: unlike post 

    data = extract_data()

    if request.method == 'GET':
        post_number = data.get('post_number')  # number of posts to be fetched
        posts = Post.query.all()

        # post_number does not exceed number of posts in the database 
        if post_number > len(posts):
            post_number = len(posts)

        random_posts = sample(posts, post_number)

        # add post data
        output = [{
            'uuid': post.uuid,
            'date_posted': post.date_posted,
            'caption': post.caption,
            'likes': len(post.liked_by),
            'image_url': f'/post_images/{post.uuid}'
        } for post in random_posts]
        
        return custom_response(True, 'Got post data', data=output)


    elif request.method == 'POST':
        action = data.get('action')
        
        if action == 'LIKE':
            post_uuid = data.get('uuid')
            
            if type(post_id) != int:
                return custom_response(False, 'Invalid post_id')
            
            target_post = Post.query.filter_by(uuid = post_uuid)
            liker = User.query.filter_by(username = data.get('liker')).first() #user that likes the post 
            
            # check if target post exists
            if not target_post:
                return custom_response(False, 'Post does not exist')
            
            # check if user has already liked the post
            current_likes = target_post.liked_by 
            
            for like in current_likes:
                if like.user_id == liker.id:
                    return custom_response(False, 'You have already liked the post')
            
            # use id instead of uuid since ids will take up less space than uuids
            like = Like(user_id = liker.id, post_id = target_post.id)
            db.session.add(like)
            db.session.commit()
            
            return custom_response(True, 'Liked post successfully')
        
        elif action == 'UNLIKE':
            # implement unlike functionality
            pass 
        else:
            return custom_response(False, 'Invalid action')
            
        # implement other features in the future such as sharing and saving 


@app.route('/images')
def get_image():
    path = request.args.get('path')

    if path:
        folder = path.split('/')

        if folder[0] == 'clothing_images' or folder[0] == 'post_images' and len(folder) == 2:
            return send_file(path, mimetype='image/gif')
        else:
            return custom_response(False, 'Invalid file path')
    else:
        return custom_response(False, 'You must give an image path')
