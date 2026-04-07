from pydantic import BaseModel
from datetime import datetime


class UserDB(BaseModel):
    name : str
    password_hash : str
    email : str | None
    admin: bool