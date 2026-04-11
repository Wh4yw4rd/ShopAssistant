from fastapi import APIRouter
from app.externals.sumup import *

router = APIRouter()

@router.get("/transactions/")
def temp_transactions():
    transactions = get_transactions()
    return {"message": transactions}