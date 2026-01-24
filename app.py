from fastapi import FastAPI, HTTPException
import uvicorn

from models import LoginCredentials, CreateUser, DBUser
from security import hash
from db_functions import add_user_to_db


app = FastAPI()


@app.get("/")
def index():
    return {"message": "Hello World!"}

# For posting login details. Returns hashed password to test hashing was successful (WILL BE REMOVED IN FINAL)

@app.post("/login/")
def login(credentials : LoginCredentials):
    hashed_password = hash(credentials.password)
    return {"username" : credentials.name, 
            "secure_password" : hashed_password}

@app.post("/create-user/")
def create_user(credentials : CreateUser):

    hashed_password = hash(credentials.password)

    user = DBUser(
        name = credentials.name,
        password_hash = hashed_password,
        email = credentials.email)
    try:
        add_user_to_db(user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"message" : "User created successfully"}