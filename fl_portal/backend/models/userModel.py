from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    username: str
    type: str
    group: str
    topology: str
    password: str
    email: EmailStr

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
