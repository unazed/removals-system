from ..exceptions.auth_exceptions import (
    InvalidCredentialsError,
    UserAlreadyExistsError
)
from . import db

from typing import final


@final
class User:
    def __init__(
        self,
        email: str,
        password: str,
        *,
        token_role_pair: tuple[str, str] | None = None
    ) -> None:
        if token_role_pair is not None:
            print("Logged in with token-pair")
            self.token, self.role = token_role_pair
            return
        print(f"Trying to login with {email=}, {password=}")
        query = db.proc_login_user(email, password)
        if query is None:
            raise InvalidCredentialsError
        self.token, self.role = query

    @classmethod
    def from_token(cls: type["User"], token: str, role: str) -> "User":
        return cls("", "", token_role_pair=(token, role))


def exists_email(email: str) -> bool:
    return db.proc_exists_email(email)


def is_valid_email(email: str) -> bool:
    return db.proc_is_valid_email(email)


def register_user(**details) -> User:
    token_role_pair = db.proc_register_user(**details)
    return User.from_token(*token_role_pair)