from app.schemas.session_schemas import *
from app.models.session_models import *
from app.models.errors import DatabaseQueryError, InvalidSession


def get_session(session_id: str, conn):
    get_session = """
        SELECT *
        FROM sessions
        WHERE session_id = %s;
    """

    try:
        with conn.cursor() as cur:
            cur.execute(get_session, (session_id,))
            session = cur.fetchone()
    
    except Exception:
        raise DatabaseQueryError("Invalid session database query.")

    if session is None:
        raise InvalidSession()
    
    session = SessionDB(
        id=session[0],
        name=session[1],
        email=session[2],
        admin=session[3],
        created_date=session[4]
    )

    return session


def add_session(new_session: Session, conn):
    import_session = """
            INSERT INTO sessions (session_id, name, email, admin)
            VALUES (%s, %s, %s, %s);
    """

    try:
        with conn.cursor() as cur:
            cur.execute(import_session, (new_session.session_id, new_session.name, new_session.email, new_session.admin,))

        conn.commit()

    except Exception:
        conn.rollback()
        raise DatabaseQueryError("Unable to import session into database.")
    

def remove_session(old_id: int, conn):
    delete_session = """
            DELETE FROM sessions
            WHERE session_id = %s; 
    """

    try:
        with conn.cursor() as cur:
            cur.execute(delete_session, (old_id,))

        conn.commit()
        
    except Exception:
        conn.rollback()
        raise DatabaseQueryError("Unable to remove session from database.")
