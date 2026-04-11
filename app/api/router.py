from fastapi import APIRouter


from app.api.endpoints import home, auth, transactions

api_router = APIRouter()

api_router.include_router(home.router, prefix="", tags=["home"])
api_router.include_router(auth.router, prefix="/user", tags=["user"])
api_router.include_router(transactions.router, prefix="/data", tags=["data"])