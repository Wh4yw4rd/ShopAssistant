from pydantic import BaseModel
from datetime import datetime

class SessionDB(BaseModel):
    id: str
    name: str
    email: str | None
    admin: bool
    created_date: datetime