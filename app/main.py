from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.router import api_router
from app.database.connections import *


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pool = initialise_pool()
    app.state.sessions = {}
    yield 
    app.state.pool.closeall()


app = FastAPI(lifespan=lifespan)

app.include_router(api_router, prefix="")
