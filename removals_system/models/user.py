from ..exceptions.auth_exceptions import InvalidCredentialsError
from . import db

from typing import final


@final
class User:
    def __init__(self, email: str, password: str) -> None:
        self.jwt_token = db.proc_login_user(email, password)
        if self.jwt_token is None:
            raise InvalidCredentialsError