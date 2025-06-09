from psycopg2.extras import DictRow


from psycopg2.extras import DictRow
import psycopg2
import psycopg2.extras

from ..config.settings import DB_CONFIG

from datetime import datetime


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


def proc_login_user(email: str, password: str) -> list[str] | None:
    return call_proc("login_user", (email, password))


def proc_register_user(
    forename: str, surname: str,
    email: str, password: str,
    dob: datetime,
    role: str | None = None,
) -> list[DictRow] | None:
    return call_proc("register_user", params=(
        forename, surname, email, dob, password, role
    ))


def proc_is_valid_email(email: str) -> bool:
    return call_proc("is_valid_email", params=(email,))[0]


def proc_exists_email(email: str) -> bool:
    return call_proc("exists_email", params=(email,))[0]
    
    
