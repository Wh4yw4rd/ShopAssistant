from fastapi import APIRouter, Depends, HTTPException, Response, Cookie

from app.database.connections import get_conn
from app.models.user_models import *
from app.schemas.user_schemas import *
from app.functions.auth import *
from app.functions.users import *


session_TTL = 86400 # 24 hours (in seconds)

router = APIRouter()

@router.post("/login/")
async def login(response: Response, user_login: UserLogin, conn = Depends(get_conn), session_id: str | None = Cookie(default=None)):

    session = check_session(str(session_id), conn)

    if session is not None:
        return {"message": f"Already logged in {session.name}!"}

    else:
        session_id = authenticate_user(user_login, conn)
        response.set_cookie(key = "session_id", value = session_id, max_age = session_TTL, httponly = True, secure = False, samesite = "lax")
        return {"message": f"Welcome, {user_login.name}!"}
    

@router.post("/logout/")
async def logout(response: Response, conn = Depends(get_conn), session_id: str | None = Cookie(default=None)):
    session = check_session(str(session_id), conn)

    if session is None:
        return {"message": "No login detected!"}
    
    else:
        logout_user(session_id, conn)
        response.delete_cookie(key = "session_id")
        return {"message": f"{session.name} has been logged out!"}
    

@router.post("/create-user/")
def create_user(new_user: NewUser, conn = Depends(get_conn), session_id: str | None = Cookie(default=None)):
    session = check_session(str(session_id), conn)

    if session is None:
        return {"message": "Unable to create user, please sign in to an admin account."}
    
    elif not session.admin:
        return {"message": f"{session.name} is not an admin, please login to an admin account."}
    
    else:
        create_user(new_user, conn)
        return {"message": f"{new_user.name} created!"}
    

@router.post("/delete-user/")
def delete_user(old_user: UserLogin, conn = Depends(get_conn), session_id: str | None = Cookie(default=None)):
    session = check_session(str(session_id), conn)

    if session is None:
        return {"message": "Unable to delete user, please sign in to an admin account."}
    
    elif not session.admin:
        return {"message": f"{session.name} is not an admin, please login to an admin account."}
    
    else:
        delete_user(old_user.name, conn)
        return {"message": f"{old_user.name} deleted!"}
    


