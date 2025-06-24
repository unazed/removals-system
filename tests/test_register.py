from psycopg2 import errors
import pytest

from removals_system.models import db

from datetime import datetime
import uuid


def random_email() -> str:
    return f"user_{uuid.uuid4().hex[:8]}@example.com"


def test_register_invalid_email(db_guest_cursor):
    with pytest.raises(errors.RaiseException):
        db.proc_register_user(
            "John", "Doe",
            "not-an-email",
            "password123",
            datetime(2000, 1, 1).date(),
            "customer"
        )


def test_register_underage(db_guest_cursor):
    with pytest.raises(errors.CheckViolation):
        db.proc_register_user(
            "John", "Doe",
            random_email(),
            "password123",
            datetime.now().date(),
            "customer"
        )


def test_register_invalid_role(db_guest_cursor):
    with pytest.raises(errors.RaiseException):
        db.proc_register_user(
            "Jane", "Smith",
            random_email(),
            "password123",
            datetime(2000, 1, 1).date(),
            "alien"
        )


def test_register_valid_account(db_guest_cursor):
    result = db.proc_register_user(
        "Alice", "Walker",
        random_email(),
        "password123",
        datetime(2000, 1, 1).date(),
        "customer"
    )
    assert result.success, "Registration should succeed"
    assert result.data.token
    assert result.data.user_role == "customer"


def test_register_duplicate_email(db_guest_cursor):
    email = random_email()

    first = db.proc_register_user(
        "Bob", "Builder",
        email,
        "password123",
        datetime(2000, 1, 1).date(),
        "customer"
    )
    assert first.success

    second = db.proc_register_user(
        "Bob", "Builder",
        email,
        "password123",
        datetime(2000, 1, 1).date(),
        "customer"
    )
    assert not second.success
    assert second.error.code == "EMAIL_EXISTS"
