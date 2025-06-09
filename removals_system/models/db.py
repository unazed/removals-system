from psycopg2.extras import DictRow
import psycopg2
import psycopg2.extras

from ..config.settings import DB_CONFIG


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def call_proc(proc_name: str, params=()) -> list[DictRow] | None:
    conn = get_connection()
    try:
        with conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.callproc(proc_name, params)
                try:
                    return cur.fetchall()
                except psycopg2.ProgrammingError:
                    return
    finally:
        conn.close()