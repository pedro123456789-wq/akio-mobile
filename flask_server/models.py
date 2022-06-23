from flask_server import db

# TODO: FINISH ME
#       Relationships,
#       Cascade behaviour

# Images will refer to the name of the image, assigned via uuid, in the filesystem
# Using String(100) since i doubt usernames, sizes, passwords, etc will ever exceed 100 characters, and postgresql requires a length to be provided with String


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    hashed_password = db.Column(db.String(100), nullable=False)

    # For avatar
    clothing_id = db.Column(db.Integer, db.ForeignKey("ClothingVariant.uuid"))
    background_colour = db.Column(db.String(100), nullable=False)

    # Posts
    liked_posts = db.relationship("Like", backref="user")

    # Clothes
    owned_clothes = db.relationship("ClothingItem", backref="user")


class ClothingVariant(db.Model):
    __tablename__ = "clothing_variant"
    # Can be used to fetch the image from filesystem
    uuid = db.Column(db.String(100), primary_key=True)
    # Using as primary key will take up a bit more space in memory maybe, but means that any uuid checks can be completed instantly due to indexing (i think)

    name = db.Column(db.String(100), nullable=False)

    size_id = db.Column(db.Integer, db.ForeignKey("Size.id"), nullable=False)
    colour_id = db.Column(db.Integer, db.ForeignKey("Colour.id"), nullable=False)

    # one to many relationship with ClothingItem(junction table) to form many-to-many relationship with User
    owners = db.relationship("ClothingItem", backref="variant")


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
    # Used for accessing image file
    uuid = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False)
    poster_id = db.Column(db.Integer, db.ForeignKey("User.id"))

    liked_by = db.relationship("Like", backref="post")


class Like(db.Model):
    __tablename__ = "like"
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey(
        "Post.uuid"), primary_key=True)

    user = db.relationship("User", backref="liked_posts")
    post = db.relationship("Post", backref="liked_by")


class ClothingItem(db.Model):
    __tablename__ = "clothing_item"
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), primary_key=True)
    variant_id = db.Column(db.Integer, db.ForeignKey("ClothingVariant.uuid"), primary_key=True)

    user = db.relationship("User", backref="owned_clothes")
    variant = db.relationship("ClothingVariant", backref="owners")
