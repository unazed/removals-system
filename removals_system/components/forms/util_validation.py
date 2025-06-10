from typing import Callable
import re


RE_VALID_NAME = re.compile(r"^[a-zA-Z][a-zA-Z\'\d]*$")

def validate_name(name: str) -> bool:
    return bool(re.match(RE_VALID_NAME, name))


def validate_password(password_getter: Callable[[], str], confirm: str) -> bool:
    return password_getter() == confirm