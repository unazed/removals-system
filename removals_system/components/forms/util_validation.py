from PySide6.QtCore import QDate

from typing import Callable, TYPE_CHECKING

import re


RE_VALID_NAME = re.compile(r"^[a-zA-Z][a-zA-Z\'\d]*$")


def validate_name(name: str) -> bool:
    return bool(re.match(RE_VALID_NAME, name))


def validate_password(password_getter: Callable[[], str], confirm: str) -> bool:
    return password_getter() == confirm


def validate_age_over_18(birth_date: "QDate") -> bool:
    if not birth_date.isValid():
        return False
    
    today = QDate.currentDate()
    age_years = today.year() - birth_date.year()
    
    if (today.month(), today.day()) < (birth_date.month(), birth_date.day()):
        age_years -= 1
    
    return age_years >= 18