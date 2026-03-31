from app.models.user_models import *


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
    
    except Exception as e:
        raise RuntimeError("Database Error")
    
    if user_data is None:
        raise ValueError("User Not Found")
    
    user_entry = UserEntry(
        name = user_data[0],
        password_hash = user_data[1],
        email = user_data[2],
        admin = user_data[3]
    )

    return user_entry
