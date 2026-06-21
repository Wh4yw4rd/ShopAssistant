from fastapi import Depends, HTTPException, Response
from database.connections_db import get_conn
from functions.auth import check_session
from models.errors import DatabaseQueryError, InvalidSession


def find_session(session_id: str | None, conn, session_required: bool = True, require_admin: bool = False):
    try:
        session = check_session(str(session_id), conn)

        if require_admin and not session.admin:
            raise {"message":"This action requires admin level."}
        
        return session

    except DatabaseQueryError:
        raise {"message":"Issue Connecting to DB."}
    
    except InvalidSession:
        if session_required:
            raise {"message": "No valid session found."}
        else:
            return None