# TODO: FINISH ME
#       Relationships,
#       Cascade behaviour

# Images will refer to the name of the image, assigned via uuid, in the filesystem
# Using String(100) since i doubt usernames, sizes, passwords, etc will ever exceed 100 characters, and postgresql requires a length to be provided with String

class User(Model):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)

    # For avatar
    clothing_id = Column(Integer, ForeignKey("ClothingVariant.uuid"))
    background_colour = Column(String(100), nullable=False)

    # Posts
    liked_posts = relationship("Like", back_populates="user")

    # Clothes
    owned_clothes = relationship("ClothingItem", back_populates="user")

class ClothingVariant(Model):
    __tablename__ = "clothing_variant"
    uuid = Column(String(100), primary_key=True)  # Can be used to fetch the image from filesystem
    # Using as primary key will take up a bit more space in memory maybe, but means that any uuid checks can be completed instantly due to indexing (i think)

    name = Column(String(100), nullable=False)

    size_id = Column(Integer, ForeignKey("Size.id"), nullable=False)
    colour_id = Column(Integer, ForeignKey("Colour.id"), nullable=False)

    owners = relationship("ClothingItem", back_populates="variant")


class Size(Model):
    __tablename__ = "size"
    id = Column(Integer, primary_key=True)
    size = Column(String(100), nullable=False, unique=True)


class Colour(Model):
    __tablename__ = "colour"
    id = Column(Integer, primary_key=True)
    colour = Column(String(100), nullable=False, unique=True)


class Post(Model):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True) # Don't use uuid, because the association table Like, will repeat a long uuid lots of times in memory which is probs not good
    uuid = Column(String(100), nullable=False)  # Used for accessing image file
    date_posted = Column(DateTime, nullable=False)
    poster_id = Column(Integer, ForeignKey("User.id"))

    liked_by = relationship("Like", back_populates="post")


class Like(Model):
    __tablename__ = "like"
    user_id = Column(Integer, ForeignKey("User.id"), primary_key=True)
    post_id = Column(Integer, ForeignKey("Post.uuid"), primary_key=True)

    user = relationship("User", back_populates="liked_posts")
    post = relationship("Post", back_populates="liked_by")


class ClothingItem(Model):
    __tablename__ = "clothing_item"
    user_id = Column(Integer, ForeignKey("User.id"), primary_key=True)
    variant_id = Column(Integer, ForeignKey("ClothingVariant.uuid"), primary_key=True)

    user = relationship("User", back_populates="owned_clothes")
    variant = relationship("ClothingVariant", back_populates="owners")