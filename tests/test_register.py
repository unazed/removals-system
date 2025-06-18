import pytest
import psycopg2.errors as errors

from datetime import datetime
import logging
g_logger = logging.getLogger(__name__)


def test_register_invalid_email(db_cursor):
    with pytest.raises(errors.RaiseException) as exc_info:
        db_cursor.callproc("register_user", (
            "p_first_name",
            "p_last_name",
            "invalid-email",
            datetime(2000, 1, 1).date(),
            "p_password",
            "customer",
        ))
    assert "Invalid email address" in str(exc_info.value)


def test_register_underage(db_cursor):
    with pytest.raises(errors.CheckViolation):
        db_cursor.callproc("register_user", (
            "p_first_name",
            "p_last_name",
            "a@a.com",
            datetime.now().date(),
            "p_password",
            "customer",
        ))


def test_register_invalid_role(db_cursor):
    with pytest.raises(errors.RaiseException) as exc_info:
        db_cursor.callproc("register_user", (
            "p_first_name",
            "p_last_name",
            "a@a.com",
            datetime(2000, 1, 1).date(),
            "p_password",
            "p_user_role",
        ))
    assert "Unhandled user role" in str(exc_info.value)


def test_register_valid_account(db_cursor):
    db_cursor.callproc("register_user", (
        "p_first_name",
        "p_last_name",
        "a@a.com",
        datetime(2000, 1, 1).date(),
        "p_password",
        "customer",
    ))
    assert db_cursor.fetchone()[0], "Registration should pass successfully"


def test_register_duplicate_email(db_cursor):
    db_cursor.callproc("register_user", (
        "p_first_name",
        "p_last_name",
        "a@a.com",
        datetime(2000, 1, 1).date(),
        "p_password",
        "customer",
    ))
    db_cursor.callproc("register_user", (
        "p_first_name",
        "p_last_name",
        "a@a.com",
        datetime(2000, 1, 1).date(),
        "p_password",
        "customer",
    ))
    assert db_cursor.fetchone()[1].code == "EMAIL_EXISTS", \
        "Cannot register with existing email"