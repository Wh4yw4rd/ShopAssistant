from psycopg2.errors import UniqueViolation

from app.schemas.user_schemas import *
from app.models.errors import DatabaseQueryError, InvalidUser, NameAlreadyExists


def get_user_credentials(name: str, conn):

    get_user = """
                SELECT name, 
                password_hash, 
                email,
                admin
                FROM users
                WHERE name = %s;
                """
    try:
        with conn.cursor() as cur:
            cur.execute(get_user, (name,))
            user_data = cur.fetchone()

        if user_data is None:
            raise InvalidUser()
    
        user_entry = UserDB(
            name = user_data[0],
            password_hash = user_data[1],
            email = user_data[2],
            admin = user_data[3]
        )

        return user_entry

    except Exception:
        conn.rollback()
        raise DatabaseQueryError("Unable to get user data.")
    
    


def add_user(new_user: UserDB, conn):
    create_new = """
                INSERT INTO users (name, password_hash, email, admin)
                VALUES (%s, %s, %s, %s);
                """
    try:
        with conn.cursor() as cur:
            cur.execute(create_new, (new_user.name, new_user.password_hash, new_user.email, new_user.admin,))

        conn.commit()

    except UniqueViolation:
        conn.rollback()
        raise NameAlreadyExists

    except Exception:
        conn.rollback()
        raise DatabaseQueryError("Unable to create new user.")


def remove_user(name: str, conn):
    delete_user = """
                DELETE FROM TABLE users
                WHERE name = %s;
                """
    
    try:
        with conn.cursor() as cur:
            cur.execute(delete_user, (name,))

        conn.commit()

    except Exception:
        conn.rollback()
        raise DatabaseQueryError("Unable to delete User.")