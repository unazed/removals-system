from psycopg2.extras import DictRow
import psycopg2
import psycopg2.extras

from ..config.settings import DB_CONFIG

from typing import (
    TypeVar, Generic, Optional, Type, Sequence, Literal, overload,
    TYPE_CHECKING
)
from dataclasses import dataclass
import json

if TYPE_CHECKING:
    from datetime import datetime


T = TypeVar('T')

@dataclass
class DbError:
    code: str
    message: str

@dataclass
class DbResult(Generic[T]):
    success: bool
    data: T | None = None
    error: DbError | None = None
    
    @classmethod
    def from_db(cls, data: list) -> 'DbResult[T]':
        if data[0]:
            return cls(success=data[0], data=data[2])
        return cls(
            success=data[0],
            error=DbError(code=data[1].code, message=data[1].message)
        )


@dataclass
class AuthenticationData:
    token: str
    user_role: str


@dataclass
class PhoneNumberData:
    phone_extension: str
    phone_number: str
    phone_number_type: str


@dataclass
class AddressData:
    line_1: str
    line_2: str
    line_3: str
    post_code: str
    address_type: str
    city_name: str
    county_name: str
    country_name: str


@dataclass
class BusinessStaffRole:
    role: str


@dataclass
class EmptyData:
    pass


def call_proc(
    proc_name: str,
    params: Sequence[object] = (),
    *,
    flatten: bool = False,
    fetch_all: bool = False,
    composites: Sequence[str] | None = None
) -> list[DictRow]:
    try:
        with (
            psycopg2.connect(**DB_CONFIG) as conn,
            conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur
        ):
            if composites is not None:
                for comp in composites:
                    psycopg2.extras.register_composite(comp, conn)
            cur.callproc(proc_name, params)
            if fetch_all:
                result = cur.fetchall()
                if flatten:
                    result = [i[0] for i in result]
                return result
            return cur.fetchone()
    finally:
        conn.close()


@overload
def call_proc_result(
    result_t: Type[T],
    proc_name: str,
    params: tuple = ...,
    *,
    is_aggregate: Literal[False] = False
) -> DbResult[T]: ...


@overload
def call_proc_result(
    result_t: Type[T],
    proc_name: str,
    params: tuple = ...,
    *,
    is_aggregate: Literal[True]
) -> DbResult[list[T]]: ...


def call_proc_result(
    result_t: Type[T],
    proc_name: str,
    params: tuple = (),
    *,
    is_aggregate: bool = False
) -> DbResult[T] | DbResult[list[T]]:
    row = DbResult.from_db(call_proc(
        proc_name, params, composites=("error_t", "result_t")
    ))
    if row.success:
        if is_aggregate:
            row.data = list(map(result_t, row.data))
        else:
            row.data = result_t(**(row.data or {}))
    return row


def proc_login_user(email: str, password: str) -> DbResult[AuthenticationData]:
    return call_proc_result(
        AuthenticationData,
        "login_user", params=(email, password)
    )


def proc_register_user(
    forename: str,
    surname: str,
    email: str,
    password: str,
    dob: "datetime",
    role: str
) -> DbResult[AuthenticationData]:
    return call_proc_result(
        AuthenticationData,
        "register_user", (forename, surname, email, dob, password, role)
    )


def proc_is_valid_email(email: str) -> bool:
    return call_proc("is_valid_email", params=(email,))[0]


def proc_exists_email(email: str) -> bool:
    return call_proc("exists_email", params=(email,))[0]
    

def proc_get_countries() -> list[str]:
    return call_proc(
        "get_countries",
        params=(),
        fetch_all=True
    )


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
    )[0]


def proc_forgot_password(
    code: str,
    email: str,
    password: str
) -> DbResult[AuthenticationData]:
    return call_proc_result(
        AuthenticationData,
        "forgot_password", params=(code, email, password)
    )


def proc_create_user_phone_number(
    token: str,
    extension: str,
    number: str,
    phone_type: str = "home"
) -> DbResult:
    return call_proc_result(
        EmptyData, "create_user_phone_number",
        params=(token, extension, number, phone_type)
    )


def proc_create_user_address(
    token: str,
    line_1: str, line_2: str, line_3: str,
    city: str, county: str, country: str, post_code: str,
    address_type: str = "home"
) -> DbResult:
    return call_proc_result(
        EmptyData, "create_user_address",
        params=(
            token,
            line_1, line_2, line_3,
            city, county, country,
            post_code, address_type
        )
    )


def proc_get_user_phone_numbers(token: str) -> DbResult[list[PhoneNumberData]]:
    return call_proc_result(
        PhoneNumberData, "get_user_phone_numbers",
        params=(token,),
        is_aggregate=True
    )


def proc_get_user_addresses(token: str) -> DbResult[list[AddressData]]:
    return call_proc_result(
        AddressData, "get_user_addresses",
        params=(token,),
        is_aggregate=True
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


def proc_create_business(
    token: str,
    business_name: str,
    crn_no: str,
    vat_no: str,
    utr_no: str,
    num_employees: int
) -> DbResult:
    return call_proc_result(
        EmptyData, "create_business",
        params=(token, business_name, crn_no, vat_no, utr_no, num_employees)
    )


def proc_add_business_resource(
    token: str,
    crn_no: str,
    resource_name: str,
    quantity: int
) -> DbResult:
    return call_proc_result(
        EmptyData, "add_business_resource",
        params=(token, crn_no, resource_name, quantity)
    )


def proc_get_business_staff_role(
    token: str,
    crn_no: str
) -> DbResult[BusinessStaffRole]:
    return call_proc_result(
        BusinessStaffRole, "get_business_staff_role",
        params=(token, crn_no)
    )