from fastapi import APIRouter


from api.endpoints import home, auth, transactions, predictions

api_router = APIRouter()

api_router.include_router(home.router, prefix="", tags=["home"])
api_router.include_router(auth.router, prefix="/user", tags=["user"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["data"])
api_router.include_router(predictions.router, prefix="/predict", tags=["predict"])