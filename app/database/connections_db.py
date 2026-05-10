from psycopg2.pool import ThreadedConnectionPool
from fastapi import Request

from app.core.config import db_config
from app.models.errors import DatabaseStartupError, DatabaseConnectionError

def initialise_pool():
    """
    Initialises connection pool to database
    """
    try:
        return ThreadedConnectionPool(
            minconn=1,
            maxconn=5,
            **db_config
        )
    except Exception:
        raise DatabaseStartupError()


def get_conn(request: Request):
    try:
        conn = request.app.state.pool.getconn()
    except Exception:
        raise DatabaseConnectionError()

    try:
        yield conn
    finally:
        request.app.state.pool.putconn(conn)
    


