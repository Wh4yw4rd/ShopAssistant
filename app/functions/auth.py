from app.schemas.user_schemas import *
from app.core.security import *
from app.database.user import *
from app.sessions.sessions import *


def create_session(user_entry: UserEntry):
    pass


def authenticate_credentials(app, user_login: UserLogin, conn):

    user_entry = get_user_credentials(user_login.name, conn)

    if not password_verify(user_login.password, user_entry.password_hash):
        raise ValueError("Invalid Credentials")
    
    else:
        id = create_session(user_entry)
        return id


