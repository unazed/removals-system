from psycopg2.extras import DictRow
import psycopg2
import psycopg2.extras

from ..config.settings import DB_CONFIG

from typing import TypeVar, Generic, Optional, Any, TYPE_CHECKING
from dataclasses import dataclass
import json

if TYPE_CHECKING:
    from datetime import datetime


T = TypeVar('T')

@dataclass
class DbResult(Generic[T]):
    success: bool
    data: Optional[T] = None
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    
    @classmethod
    def success_result(cls, data: T) -> 'DbResult[T]':
        return cls(success=True, data=data)
    
    @classmethod
    def error_result(cls, error_code: str, error_message: str) -> 'DbResult[T]':
        return cls(
            success=False,
            error_code=error_code,
            error_message=error_message
        )


@dataclass
class AuthenticationData:
    token: str
    user_role: str
    user_id: int


@dataclass
class PhoneNumberData:
    phone_number_id: int
    phone_extension: str
    phone_number: str
    phone_number_type: str


@dataclass
class AddressData:
    address_id: int
    line_1: str
    line_2: str
    line_3: str
    post_code: str
    address_type: str
    city_name: str
    county_name: str
    country_name: str


def call_proc(
    proc_name: str,
    params=(),
    *,
    flatten: bool = False,
    fetch_all: bool = False
) -> list[DictRow]:
    try:
        with (
            psycopg2.connect(**DB_CONFIG) as conn,
            conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur
        ):
            cur.callproc(proc_name, params)
            if fetch_all:
                result = cur.fetch_all()
                if flatten:
                    result = [i[0] for i in result]
                return result
            return cur.fetchone()
    finally:
        conn.close()


def call_proc_result(
    proc_name: str,
    params: tuple = ()
) -> DbResult:
    return DbResult(call_proc(proc_name, params))


def proc_login_user(email: str, password: str) -> DbResult[AuthenticationData]:
    row = call_proc_result("login_user", (email, password))
    print(row)
    if row.success:
        data = json.loads(row.data)
        return DbResult.success_result(AuthenticationData(
            token=data['token'],
            user_role=data['user_role'],
        ))

    return DbResult.error_result(row.error.code, row.error.message)


def proc_register_user(
    forename: str,
    surname: str,
    email: str,
    password: str,
    dob: "datetime",
    role: str
) -> DbResult[AuthenticationData]:
    row = call_proc("register_user", (
        forename, surname, email, dob, password, role
    ))
    
    if row.success:
        data = json.loads(row.data)
        return DbResult.success_result(AuthenticationData(
            token=data['token'],
            user_role=data['user_role'],
        ))

    return DbResult.error_result(row.error.code, row.error.message)


def proc_is_valid_email(email: str) -> bool:
    return call_proc("is_valid_email", params=(email,))


def proc_exists_email(email: str) -> bool:
    return call_proc("exists_email", params=(email,))
    

def proc_get_countries() -> list[str]:
    return call_proc("get_countries", params=())


def proc_get_counties(country_name: str) -> list[str]:
    return call_proc(
        "get_counties",
        params=(country_name,),
        fetch_all=True,
        flatten=True
    )


def proc_get_cities(country_name: str, county_name: str) -> list[str]:
    return call_proc(
        "get_cities",
        params=(country_name, county_name),
        fetch_all=True,
        flatten=True
    )


def proc_get_length_constraint(table: str, column: str) -> int:
    return call_proc(
        "get_length_constraint",
        params=(table, column)
    )


def proc_forgot_password(
    code: str,
    email: str,
    password: str
) -> DbResult[AuthenticationData]:
    row = call_proc("forgot_password", params=(code, email, password))
    
    if row.success:
        data = json.loads(row.data)
        return DbResult.success_result(AuthenticationData(
            token=data['token'],
            user_role=data['user_role'],
        ))

    return DbResult.error_result(row.error.code, row.error.message)


def proc_create_user_phone_number(
    token: str,
    extension: str,
    number: str,
    phone_type: str = "home"
) -> DbResult:
    return call_proc(
        "create_user_phone_number",
        params=(token, extension, number, phone_type)
    )


def proc_create_user_address(
    token: str,
    line_1: str, line_2: str, line_3: str,
    city: str, county: str, country: str, post_code: str,
    address_type: str = "home"
) -> DbResult:
    return call_proc(
        "create_user_address",
        params=(
            token,
            line_1, line_2, line_3,
            city, county, country,
            post_code, address_type
        )
    )


def proc_get_user_phone_numbers(token: str) -> DbResult[list[PhoneNumberData]]:
    rows = call_proc(
        "get_user_phone_numbers",
        params=(token,),
        fetch_all=True
    )

    if rows.success:
        data = json.loads(row.data)
        return DbResult.success_result([
            PhoneNumberData(number)
            for number in data
        ])

    return DbResult.error_result(rows.error.code, rows.error.message)


def proc_get_user_addresses(token: str) -> DbResult[list[AddressData]]:
    rows = call_proc(
        "get_user_addresses",
        params=(token,),
        fetch_all=True
    )

    if rows.success:
        data = json.loads(row.data)
        return DbResult.success_result([
            AddressData(number)
            for number in data
        ])

    return DbResult.error_result(rows.error.code, rows.error.message)


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


def proc_create_business(
    token: str,
    business_name: str,
    crn_no: str,
    vat_no: str,
    utr_no: str,
    num_employees: int
) -> str:
    return call_proc(
        "create_business",
        params=(token, business_name, crn_no, vat_no, utr_no, num_employees)
    )


def proc_add_business_resource(
    token: str,
    crn_no: str,
    resource_name: str,
    quantity: int
) -> str:
    return call_proc(
        "add_business_resource",
        params=(token, crn_no, resource_name, quantity)
    )


def proc_get_business_staff_role(token: str, crn_no: str) -> DictRow:
    return call_proc(
        "get_business_staff_role",
        params=(token, crn_no)
    )