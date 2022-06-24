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
