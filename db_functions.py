import psycopg2
from datetime import datetime

from models import DBUser, LoginCredentials
from data_collection import get_transactions
from config import db_config


def get_db_connection():
    """
    Establishes connection to PosgreSQL database.
    """
    return psycopg2.connect(**db_config)


def login_user(credentials : LoginCredentials):
    """
    Retrieves user data from database for login.
    """

    # Connect to database
    conn = get_db_connection()

    # Query to get user data
    get_user = """
                SELECT name, password_hash, admin
                FROM users
                WHERE name = %s;
                """

    # Execute query and save user data
    try:
        with conn.cursor() as cursor:
            cursor.execute(get_user, (credentials.name,))
            user_data = cursor.fetchone()
    
    except Exception as e:
        raise Exception("Database error: " + str(e))
    finally:
        conn.close()

    # Raise error if user not found
    if user_data is None:
        raise ValueError("User not found")
    
    # Return the user data
    return user_data

    
def add_user_to_db(user : DBUser):
    """
    Adds a new user to the database.
    """
    # Connect to database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Query to add new user
    add_user = """
                INSERT INTO users (name, password_hash, email)
                VALUES (%s, %s, %s)
               """
    
    # Execute query
    cursor.execute(add_user, (user.name, user.password_hash, user.email))
    
    # Save changes and close connection
    conn.commit()
    cursor.close()
    conn.close()


def update_transactions():
    """
    Updates transaction data in the database to include the most recent transactions.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    most_recent_transaction = """
                                SELECT timestamp
                                FROM transactions
                                ORDER BY timestamp DESC
                                LIMIT 1;
                                """
    
    cursor.execute(most_recent_transaction)
    latest_time = cursor.fetchone()

    if latest_time is None:
        latest_time = datetime(2000, 1, 1)
    
    try:
        new_transactions = get_transactions(oldest_date = latest_time[0].isoformat() + "Z")
    
    except Exception as e:
        cursor.close()
        conn.close()
        raise Exception("Error fetching transactions: " + str(e))
        
    