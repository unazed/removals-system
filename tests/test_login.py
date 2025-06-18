import logging
g_logger = logging.getLogger(__name__)


def test_login_invalid_details(db_cursor):
    db_cursor.callproc("login_user", ("a@a.com", "password"))
    assert db_cursor.fetchone()[1].code == "INVALID_CREDENTIALS"


def test_login_invalid_email(db_cursor):
    db_cursor.callproc("login_user", ("a", "password"))
    assert db_cursor.fetchone()[1].code == "INVALID_CREDENTIALS"


def test_login_valid_user(db_cursor, with_valid_user):
    email, password, _ = with_valid_user("customer")
    db_cursor.callproc("login_user", (email, password))
    assert db_cursor.fetchone()[0], "Login should've been successful"


def test_login_when_pending(db_cursor, with_valid_user):
    email, password, _ = with_valid_user("service-provider")
    db_cursor.callproc("login_user", (email, password))
    assert db_cursor.fetchone()[1].code == "PENDING_APPROVAL"