from fastapi import APIRouter, Depends, HTTPException, Cookie

from app.database.connections import get_conn
from app.schemas.user_schemas import *
from app.functions.auth import *


router = APIRouter()

@router.post("/login/")
async def login(user_login: UserLogin, conn = Depends(get_conn)):
    try:
        session_id = authenticate_credentials(user_login, conn)

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return session_id

