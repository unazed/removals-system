from ..exceptions.auth_exceptions import InvalidCredentialsError
from . import db

from typing import final


@final
class User:
    def __init__(self, email: str, password: str) -> None:
        query = db.proc_login_user(email, password)
        print(query)
        if query[0] is None:
            raise InvalidCredentialsError
        self.token, self.role = query