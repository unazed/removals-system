from removals_system.models.db import proc_login_user
import logging

g_logger = logging.getLogger(__name__)


def test_login_invalid_details(db_cursor):
    result = proc_login_user("a@a.com", "password")
    assert not result.success
    assert result.error.code == "INVALID_CREDENTIALS"


def test_login_invalid_email(db_cursor):
    result = proc_login_user("a", "password")
    assert not result.success
    assert result.error.code == "INVALID_CREDENTIALS"


def test_login_valid_user(with_valid_user):
    email, password, _ = with_valid_user("customer")
    result = proc_login_user(email, password)
    assert result.success, "Login should've been successful"
    assert result.data.token
    assert result.data.user_role == "customer"


def test_login_when_pending(with_valid_user):
    email, password, _ = with_valid_user("service-provider")
    result = proc_login_user(email, password)
    assert not result.success
    assert result.error.code == "PENDING_APPROVAL"
