from psycopg2.pool import SimpleConnectionPool
from datetime import datetime

from models import DBUser, LoginCredentials
from data_collection import get_transactions
from config import db_config


def initialise_pool():
    """
    Establishes connection pool for PostgreSQL database.
    """
    global pool 
    pool = SimpleConnectionPool(
        minconn = 1,
        maxconn = 5,
        **db_config
    )


def close_pool():
    """
    Closes connection pool down
    """
    pool.closeall()



def login_user(credentials : LoginCredentials):
    """
    Retrieves user data from database for login.
    """
    # Get connection from pool.
    conn = pool.getconn()

    # Query to get user data
    get_user = """
                SELECT name, password_hash, admin
                FROM users
                WHERE name = %s;
                """

    # Execute query and save output in user_data variable
    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(get_user, (credentials.name,))
                user_data = cursor.fetchone()
    
    except Exception as e:
        raise Exception("Database error: " + str(e))

    finally:
        # Put connection back in pool
        pool.putconn(conn)

    # Raise error if user not found
    if user_data is None:
        raise ValueError("User not found")
    
    # Return the user data
    return user_data

    
def add_user_to_db(user : DBUser):
    """
    Adds a new user to the database.
    """
    # Establish connection to database
    conn = pool.getconn()

     # Query to add new user
    add_user = """
                INSERT INTO users (name, password_hash, email)
                VALUES (%s, %s, %s)
               """
    
    # Execute query
    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(add_user, (user.name, user.password_hash, user.email))

                # Save changes to database
                conn.commit()

    # Raise exception if issues with transaction
    except Exception as e:
        raise Exception("Database error: " + str(e))
    
    # Put connection back in pool
    finally:
        pool.putconn(conn)



def update_transactions():
    """
    Updates transaction data in the database to include the most recent transactions.
    """
    # Establish connection to database
    conn = pool.getconn()

    # Query to get most recent transaction in database
    most_recent_transaction = """
                                SELECT timestamp
                                FROM transactions
                                ORDER BY timestamp DESC
                                LIMIT 1;
                                """
    
    try:
        with conn:
            with conn.cursor() as cursor:
                # Execute query to get most recent transaction date value
                cursor.execute(most_recent_transaction)
                latest_time = cursor.fetchone()

                # Set default if database is empty
                if latest_time is None:
                    latest_time = datetime(2000, 1, 1)
                
                # Retrieve all new data after latest date
                new_transactions = get_transactions(oldest_date = latest_time[0].isoformat() + "Z")
    
    except Exception as e:
        cursor.close()
        conn.close()
        raise Exception("Error fetching transactions: " + str(e))
    
    finally:
        pool.putconn(conn)
        
    