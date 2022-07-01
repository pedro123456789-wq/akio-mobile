from typing import List, Optional
from pydantic import BaseModel



"""@loginRequired"""
class SessionValidation(BaseModel):
    token: str
    username: str
    

"""/api/sign-up"""
class SignUp(BaseModel):
    username: str
    password: str
    
    
"""/api/clothing-variants => POST"""
class ClothingVariant(BaseModel):
    uuid: int
    name: str
    size: str
    colour: str


"""api/user/profile"""
class ProfileData(BaseModel):
    background_colour: str
    clothing_uuid: int 
    