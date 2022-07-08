from typing import List, Optional
from pydantic import BaseModel, validator
from flask_server.models import ClothingVariant



class SessionValidation(BaseModel):
    """@loginRequired"""
    token: str
    username: str


class SignUp(BaseModel):
    """/api/sign-up"""
    username: str
    password: str


class ClothingVariantValidator(BaseModel):
    """/api/clothing-variants => POST"""
    name: str
    size: str
    colour: str
    image_data: str


class ProfileData(BaseModel):
    """api/user/profile"""
    background_colour: str
    clothing_id: str

    @validator('clothing_id')
    def is_valid(cls, v):
        items = ClothingVariant.query.all()
        uuids = [str(item.uuid) for item in items]

        if v not in uuids:
            raise ValueError('Invalid uuid entered')

        return v


    @validator('background_colour')
    def is_hex(cls, v):
        if len(v) != 7 or v[0] != '#':
            raise ValueError('Invalid hex value')

        return v


class PostValidation(BaseModel):
    caption: str
    image_data: str
    
