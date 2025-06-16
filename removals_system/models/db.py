from psycopg2.extras import DictRow
import psycopg2
import psycopg2.extras

from ..config.settings import DB_CONFIG

from datetime import datetime


def _flatten_nested_list(l: list[list]) -> list:
    return [sub_l[0] for sub_l in l]


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def call_proc(
    proc_name: str,
    params=(),
    *,
    fetch_all: bool = False,
    flatten: bool = False
) -> list[DictRow]:
    try:
        with (
            get_connection() as conn,
            conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur
        ):
            cur.callproc(proc_name, params)
            if fetch_all:
                result = cur.fetchall()
                return _flatten_nested_list(result) if flatten else result
            val = cur.fetchone()
            return val
    finally:
        conn.close()


def proc_login_user(email: str, password: str) -> list[DictRow]:
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
    

def proc_get_countries() -> list[DictRow]:
    return call_proc("get_countries", params=(), fetch_all=True)


def proc_get_counties(country_name: str) -> list[DictRow]:
    return call_proc("get_counties", params=(country_name,), fetch_all=True)


def proc_get_cities(country_name: str, county_name: str) -> list[DictRow]:
    return call_proc(
        "get_cities",
        params=(country_name, county_name),
        fetch_all=True
    )


def proc_get_length_constraint(table: str, column: str) -> int:
    return call_proc(
        "get_length_constraint",
        params=(table, column)
    )[0]


def proc_forgot_password(code: str, email: str, password: str) -> list[DictRow]:
    return call_proc(
        "forgot_password",
        params=(code, email, password)
    )


def proc_create_user_phone_number(
    token: str,
    extension: str,
    number: str,
    phone_type: str = "home"
) -> str:
    return call_proc(
        "create_user_phone_number",
        params=(token, extension, number, phone_type)
    )[0]


def proc_create_user_address(
    token: str,
    line_1: str, line_2: str, line_3: str,
    city: str, county: str, country: str, post_code: str,
    address_type: str = "home"
) -> str:
    return call_proc(
        "create_user_address",
        params=(token, line_1, line_2, line_3, city, county, country, post_code, address_type)
    )[0]


def proc_get_user_phone_numbers(token: str) -> list[DictRow] | None:
    return call_proc(
        "get_user_phone_numbers",
        params=(token,),
        fetch_all=True
    )


def proc_get_user_addresses(token: str) -> list[DictRow] | None:
    return call_proc(
        "get_user_addresses",
        params=(token,),
        fetch_all=True
    )


def proc_get_type_values(table: str) -> list[DictRow]:
    return call_proc(
        "get_type_values",
        params=(table,),
        fetch_all=True,
        flatten=True
    )

def proc_get_type_table_names() -> list[DictRow]:
    return call_proc(
        "get_type_table_names",
        fetch_all=True,
        flatten=True
    )