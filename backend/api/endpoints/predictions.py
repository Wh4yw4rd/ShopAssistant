from fastapi import APIRouter, Depends
from datetime import datetime
from database.connections_db import get_conn
from functions.predictions import *


router = APIRouter()


@router.get("/moving-7-days/")
def moving_7_days(day: datetime, conn=Depends(get_conn)):
    prediction = moving_7_day_average(day, conn)
    return prediction