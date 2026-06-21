from fastapi import APIRouter, Depends, HTTPException
from database.connections_db import get_conn
from externals.sumup import *
from database.transactions_db import *
from functions.transactions import *

router = APIRouter()

@router.get("/update/")
def refresh_transactions(conn = Depends(get_conn)):
    num_added = update_transactions(conn, 1000)
    return {"message": f"Done! {num_added} transactions added!"}


@router.get("/range/{start}-{end}")
def transaction_from_range(start: str, end: str, conn = Depends(get_conn)):
    try:
        start = datetime.strptime(start, r"%Y%m%d")
        end = datetime.strptime(end, r"%Y%m%d")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Date Formats")
    
    data = transaction_range(start, end, conn)
    return data
