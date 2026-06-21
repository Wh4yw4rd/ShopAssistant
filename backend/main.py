from fastapi import FastAPI
from contextlib import asynccontextmanager

from api.router import api_router
from database.connections_db import *


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pool = initialise_pool()
    yield 
    app.state.pool.closeall()


app = FastAPI(lifespan=lifespan)

app.include_router(api_router, prefix="")
