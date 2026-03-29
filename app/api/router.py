from fastapi import APIRouter


from app.api.endpoints import home, auth

api_router = APIRouter()

api_router.include_router(home.router, prefix="", tags=["home"])
api_router.include_router(auth.router, prefix="/user", tags=["user"])