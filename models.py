from pydantic import BaseModel

class login_credentials(BaseModel):
    name : str
    password : str