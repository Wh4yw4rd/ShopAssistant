import psycopg2
from models import DBUser
from config import db_config

def get_db_connection():
    return psycopg2.connect(**db_config)

def add_user_to_db(user : DBUser):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    add_user = """
    INSERT INTO users (name, password_hash, email)
    VALUES (%s, %s, %s)
    """
    
    cursor.execute(add_user, (user.name, user.password_hash, user.email))
    
    conn.commit()
    cursor.close()
    conn.close()