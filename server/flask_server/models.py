from flask_server import db

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
    clothing_id = db.Column(db.Integer, db.ForeignKey("clothing_variant.uuid"), nullable = True)
    background_colour = db.Column(db.String(100), nullable=True) #hex value
    
    # posted posts 
    posts_made = db.relationship("Post", backref = "user")

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

    size_id = db.Column(db.Integer, db.ForeignKey("size.id"), nullable=False)
    colour_id = db.Column(db.Integer, db.ForeignKey("colour.id"), nullable=False)

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
    
    poster_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    liked_by = db.relationship("Like", backref="post")


class Like(db.Model):
    __tablename__ = "like"
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("post.uuid"), primary_key=True)


class ClothingItem(db.Model):
    __tablename__ = "clothing_item"
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    variant_id = db.Column(db.Integer, db.ForeignKey("clothing_variant.uuid"), primary_key=True)