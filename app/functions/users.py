from app.database.user import *
from app.models.user_models import *
from app.core.security import hash

def create_user(new_user: NewUser, conn):
    password_hash = hash(new_user.password)
    new_user_db = UserDB(new_user.name, password_hash, new_user.email, new_user.admin)

    add_user(new_user_db, conn)
