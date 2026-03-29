from psycopg2.pool import ThreadedConnectionPool
from fastapi import Request

from app.core.config import db_config

def initialise_pool():
    """
    Initialises connection pool to database
    """
    return ThreadedConnectionPool(
        minconn=1,
        maxconn=5,
        **db_config
    )


def get_conn(request: Request):
    conn = request.app.state.pool.getconn()

    try:
        yield conn
    finally:
        request.app.state.pool.putconn(conn)

