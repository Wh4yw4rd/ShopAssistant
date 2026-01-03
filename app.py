from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI()

@app.get("/")
async def index():
    return {"message": "Hello World!"}

@app.get("/hello/")
async def hello():
    return {"message" : "Hello again!"}
