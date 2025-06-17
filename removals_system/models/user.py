from ..exceptions.auth_exceptions import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
    InvalidSessionError
)
from . import db

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .businesses import Business


class User:
    def __init__(
        self,
        email: str,
        password: str,
        *,
        token_role_pair: tuple[str, str] | None = None
    ) -> None:
        if token_role_pair is not None:
            self.token, self.role = token_role_pair
            return
        result = db.proc_login_user(email, password)
        print(result)
        self.token, self.role = token_role_pair
        self.assigned_business: "Business | None" = None

    def create_address(
        self,
        city: str, county: str, country: str, post_code: str,
        line_1: str, line_2: str = "", line_3: str = "",
        address_type: str = "home"
    ) -> None:
        error = db.proc_create_user_address(
            self.token, line_1, line_2, line_3,
            city, county, country, post_code, address_type
        )

    def create_phone_number(
        self,
        extension: str, number: str,
        phone_type: str = "home"
    ) -> None:
        error = db.proc_create_user_phone_number(
            self.token, extension, number, phone_type
        )

    def get_phone_numbers(self):
        numbers = db.proc_get_user_phone_numbers(self.token)

        return numbers

    def get_addresses(self):
        addresses = db.proc_get_user_phone_numbers(self.token)

        return addresses


    @classmethod
    def from_token(cls: type["User"], token: str, role: str) -> "User":
        return cls("", "", token_role_pair=(token, role))


def exists_email(email: str) -> bool:
    return db.proc_exists_email(email)


def is_valid_email(email: str) -> bool:
    return db.proc_is_valid_email(email)


def register_user(**details) -> User:
    error, *token_role_pair = db.proc_register_user(**details)
    User.maybe_raise_exception(error)
    return User.from_token(*token_role_pair)


def forgot_password(code: str, email: str, password: str) -> "User":
    error, *token_role_pair = db.proc_forgot_password(code, email, password)
    User.maybe_raise_exception(error)
    return User.from_token(*token_role_pair)