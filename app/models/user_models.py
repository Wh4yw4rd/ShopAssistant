from pydantic import BaseModel
from datetime import datetime

class UserEntry(BaseModel):
    name : str
    password_hash : str
    email : str
    admin: bool