from . import db, db_errors

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .business import Business


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
        data = db_errors.unwrap_result(db.proc_login_user(email, password))
        self.token, self.role = data.token, data.user_role

    def create_address(
        self,
        city: str, county: str, country: str, post_code: str,
        line_1: str, line_2: str = "", line_3: str = "",
        address_type: str = "home"
    ) -> None:
        db_errors.unwrap_result(
            db.proc_create_user_address(
                self.token, line_1, line_2, line_3,
                city, county, country, post_code, address_type
            )
        )

    def create_phone_number(
        self,
        extension: str, number: str,
        phone_type: str = "home"
    ) -> None:
        db_errors.unwrap_result(
            db.proc_create_user_phone_number(
                self.token, extension, number, phone_type
            )
        )

    def get_phone_numbers(self):
        return db_errors.unwrap_result(
            db.proc_get_user_phone_numbers(self.token)
        )

    def get_addresses(self):
        return db_errors.unwrap_result(
            db.proc_get_user_addresses(self.token)
        )

    @classmethod
    def from_token(cls: type["User"], token: str, role: str) -> "User":
        return cls("", "", token_role_pair=(token, role))


def exists_email(email: str) -> bool:
    return db.proc_exists_email(email)


def is_valid_email(email: str) -> bool:
    return db.proc_is_valid_email(email)


def register_user(**details) -> User:
    data = db_errors.unwrap_result(db.proc_register_user(**details))
    return User.from_token(data.token, data.user_role)


def forgot_password(code: str, email: str, password: str) -> User:
    data = db_errors.unwrap_result(
        db.proc_forgot_password(code, email, password)
    )
    return User.from_token(data.token, data.user_role)