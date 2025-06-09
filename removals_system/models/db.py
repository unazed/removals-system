from psycopg2.extras import DictRow
import psycopg2
import psycopg2.extras

from ..config.settings import DB_CONFIG

def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def call_proc(proc_name: str, params=()) -> list[DictRow]:
    try:
        with (
            get_connection() as conn,
            conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur
        ):
            cur.callproc(proc_name, params)
            return cur.fetchone()
    finally:
        conn.close()


def proc_login_user(email: str, password: str) -> list[str | None]:
    return call_proc('login_user', (email, password))
    
    
    
