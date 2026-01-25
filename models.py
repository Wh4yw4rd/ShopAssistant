from typing import Annotated
from pydantic import BaseModel

class LoginCredentials(BaseModel):
    name : str
    password : str

class CreateUser(BaseModel):
    name : str
    password : str
    email : str = None

class DBUser(BaseModel):
    name : str
    password_hash : str
    email : str | None = None