from pydantic import BaseModel


class UserLogin(BaseModel):
    name: str
    password: str


class NewUser(BaseModel):
    name: str
    password: str
    email: str
    admin: bool