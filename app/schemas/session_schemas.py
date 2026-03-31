from pydantic import BaseModel
from datetime import datetime

class SessionDB(BaseModel):
    id: int
    name: str
    email: str
    admin: bool
    created_date: datetime