from pydantic import BaseModel
from datetime import datetime

class Cookies(BaseModel):
    session_id: str


class Session(BaseModel):
    session_id: str
    name: str
    email: str
    admin: bool