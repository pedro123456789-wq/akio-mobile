from flask_server.app import db
from datetime import datetime

# TODO: FINISH ME
#       Relationships,
#       Cascade behaviour
#       Add email to use database to avoid mass account creation

# Images will refer to the name of the image, assigned via uuid, in the filesystem
# Using String(100) since i doubt usernames, sizes, passwords, etc will ever exceed 100 characters, and postgresql requires a length to be provided with String


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    hashed_password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default = False)

    # For avatar
    # change to not nullable in future 
    clothing_id = db.Column(db.String(100), db.ForeignKey("clothing_variant.uuid"), nullable = True)
    avatar_clothing = db.relationship("ClothingVariant")

    background_colour = db.Column(db.String(100), nullable=True) # hex value

    # posted posts 
    posts = db.relationship("Post", back_populates="poster")

    # Posts
    liked_posts = db.relationship("Like", back_populates="user")

    # Clothes
    owned_clothes = db.relationship("ClothingItem", back_populates="user")


class ClothingVariant(db.Model):
    __tablename__ = "clothing_variant"
    id = db.Column(db.Integer, primary_key=True)

    # Can be used to fetch the image from filesystem
    uuid = db.Column(db.String(100), nullable=False)

    # Using as primary key will take up a bit more space in memory maybe, but means that any uuid checks can be completed instantly due to indexing (i think)
    name = db.Column(db.String(100), nullable=False)

    size_id = db.Column(db.Integer, db.ForeignKey("size.id"), nullable=False)
    size = db.relationship("Size")

    colour_id = db.Column(db.Integer, db.ForeignKey("colour.id"), nullable=False)
    colour = db.relationship("Colour")

    # one to many relationship with ClothingItem(junction table) to form many-to-many relationship with User
    owners = db.relationship("ClothingItem", back_populates="variant")


class Size(db.Model):
    __tablename__ = "size"
    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.String(100), nullable=False, unique=True)


class Colour(db.Model):
    __tablename__ = "colour"
    id = db.Column(db.Integer, primary_key=True)
    colour = db.Column(db.String(100), nullable=False, unique=True)


class Post(db.Model):
    __tablename__ = "post"
    # Don't use uuid, because the association table Like, will repeat a long uuid lots of times in memory which is probs not good
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default = datetime.utcnow())
    caption = db.Column(db.String(100), nullable = False)

    poster_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    poster = db.relationship("User", back_populates="posts")
    liked_by = db.relationship("Like", back_populates="post")


class Like(db.Model):
    __tablename__ = "like"
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    user = db.relationship("User", back_populates="liked_posts")

    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), primary_key=True)
    post = db.relationship("Post", back_populates="liked_by")



class ClothingItem(db.Model):
    __tablename__ = "clothing_item"
    id = db.Column(db.Integer, primary_key=True)

    variant_id = db.Column(db.String(100), db.ForeignKey("clothing_variant.uuid"))
    variant = db.relationship("ClothingVariant", back_populates="owners")

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    user = db.relationship("User", back_populates="owned_clothes")

    uuid = db.Column(db.String(100), nullable=False)
