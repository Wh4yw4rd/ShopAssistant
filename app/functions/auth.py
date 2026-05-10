from app.models.user_models import *
from app.schemas.user_schemas import *
from app.core.security import *
from app.database.user_db import *
from app.database.sessions_db import *
from app.models.errors import InvalidUser

import uuid


def check_session(session_id: str, conn):
    session = get_session(session_id, conn)
    return session


def authenticate_user(user_login: UserLogin, conn):

    user_db = get_user_credentials(user_login.name, conn)

    if not password_verify(user_login.password, user_db.password_hash):
        raise InvalidUser()
    
    else:
        id = str(uuid.uuid4())
        new_session = Session(
            session_id=id,
            name=user_db.name,
            email=user_db.email,
            admin=user_db.admin
        )

        add_session(new_session, conn)

        return id


def logout_user(session_id: str, conn):
    remove_session(session_id, conn)
    


    
