from fastapi import APIRouter, Depends, HTTPException, Response, Cookie

from database.connections_db import get_conn
from models.user_models import *
from schemas.user_schemas import *
from functions.auth import *
from functions.users import *
from api.dependencies.auth import find_session


session_TTL = 86400 # 24 hours (in seconds)

router = APIRouter()

@router.post("/login/")
async def login_endpoint(response: Response, user_login: UserLogin, conn = Depends(get_conn), session_id: str | None = Cookie(default=None)):

    session = find_session(session_id, conn, session_required = False)

    if session is not None:
        return {"message": f"Already logged in {session.name}!"}
    
    try:
        session_id = authenticate_user(user_login, conn)
        response.set_cookie(key = "session_id", value = session_id, max_age = session_TTL, httponly = True, secure = False, samesite = "lax")
        return {"message": f"Welcome, {user_login.name}!"}
    except InvalidUser:
        return {"message": "Incorrect login credentials."}
    except DatabaseQueryError:
        return {"message": "Error connecting to database."}
 

@router.post("/logout/")
async def logout_endpoint(response: Response, conn = Depends(get_conn), session_id: str | None = Cookie(default=None)):
    session = find_session(session_id, conn)

    try:
        logout_user(session_id, conn)
        response.delete_cookie(key = "session_id")
        return {"message": f"{session.name} has been logged out!"}
    
    except DatabaseQueryError:
        return {"message": "Error Connecting to database."}
    

@router.post("/create-user/")
def create_user_endpoint(new_user: NewUser, conn = Depends(get_conn), session_id: str | None = Cookie(default=None)):
    session = find_session(session_id, conn, require_admin = True)
    
    try:
        create_user(new_user, conn)
        return {"message": f"{new_user.name} created!"}
    
    except NameAlreadyExists as e:
        return {"message": str(e)}
    
    except DatabaseQueryError:
        return {"message": "Unable to connect to database."}
    

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
    


