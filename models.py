from typing import Annotated
from pydantic import BaseModel
from datetime import datetime

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

class Cookies(BaseModel):
    session_id : str


class Transaction(BaseModel):
    transaction_code : str
    amount : float
    status : str
    payment_type : str
    entry_mode : str
    timestamp : datetime