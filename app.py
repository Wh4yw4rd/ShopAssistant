from fastapi import FastAPI, HTTPException
import uvicorn

from models import login_credentials
from security import hash

app = FastAPI()

@app.get("/")
def index():
    return {"message": "Hello World!"}

@app.get("/hello/")
def hello():
    return {"message" : "Hello again!"}

@app.get("/hello/{name}/")
def name_hello(name :str):
    return {"message" : f"Hello, {name}!"}

# For posting login details. Returns hashed password to test hashing was successful (WILL BE REMOVED IN FINAL)

@app.post("/login/")
def login(credentials : login_credentials):
    hashed_password = hash(credentials.password)
    return {"username" : credentials.name, 
            "secure_password" : hashed_password}
