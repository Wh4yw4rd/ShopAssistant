from database.user_db import *
from models.user_models import *
from core.security import *
from models.errors import AdminRequired


def create_user(new_user: NewUser, conn):
    password_hash = hash(new_user.password)
    new_user_db = UserDB(name = new_user.name,
                         password_hash = password_hash, 
                         email = new_user.email, 
                         admin = new_user.admin)
    add_user(new_user_db, conn)


def delete_user(name: str, admin: bool, remove_name: str, conn):
    if not admin and name != remove_name:
        raise AdminRequired("Admin account required to remove users.")

    user_entry = get_user_credentials(remove_name, conn)

    remove_user(remove_name)
