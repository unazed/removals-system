from ..exceptions.auth_exceptions import (
    InvalidCredentialsError,
    UserAlreadyExistsError
)
from . import db

from typing import final


@final
class User:
    def __init__(self, email: str, password: str) -> None:
        query = db.proc_login_user(email, password)
        if query is None:
            raise InvalidCredentialsError
        self.token, self.role = query


def exists_email(email: str) -> bool:
    return db.proc_exists_email(email)


def is_valid_email(email: str) -> bool:
    return db.proc_is_valid_email(email)


def register_user(**details) -> None:
    result = db.proc_register_user(**details)