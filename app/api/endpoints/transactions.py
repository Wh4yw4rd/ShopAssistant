from fastapi import APIRouter, Depends
from app.database.connections import get_conn
from app.externals.sumup import *
from app.database.transactions import *
from app.functions.transactions import *

router = APIRouter()

@router.get("/transactions/")
def temp_transactions(conn = Depends(get_conn)):
    update_transactions(conn, 1000)
    return {"message": "Done!"}