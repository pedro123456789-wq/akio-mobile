# TODO: FINISH ME

# Images will refer to the name of the image, assigned via uuid, in the filesystem

class User(Model):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)


class ClothingVariant(Model):
    __tablename__ = "clothing_variant"
    uuid = Column(String, primary_key=True)  # Can be used to fetch the image from filesystem
    # Using as primary key will take up a bit more space in memory maybe, but means that any uuid checks can be completed instantly due to indexing (i think)

    size_id = Column(Integer, ForeignKey('size.id'), nullable=False)
    colour_id = Column(Integer, ForeignKey('colour.id'), nullable=False)


class Size(Model):
    __tablename__ = "size"
    id = Column(Integer, primary_key=True)
    info = Column(String, nullable=False, unique=True)

    # todo: define relationship to get all clothingvariants of a specified colour


class Colour(Model):
    __tablename__ = "colour"
    id = Column(Integer, primary_key=True)
    colour = Column(String, nullable=False, unique=True)

    # todo: define relationship to get all clothingvariants of a specified size


# Many to many relationship middle table
class AvatarInfo(db.Model):
    clothing_id = Column(Integer, ForeignKey('clothingvariant.uuid'))
    user_id = Column(Integer, ForeignKey('user.id'))

    # todo: relationship
