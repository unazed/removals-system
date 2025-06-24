from psycopg2 import errors
import pytest

import logging
g_logger = logging.getLogger(__name__)


def test_guest_role_is_active(db_guest_cursor):
    db_guest_cursor.execute("SELECT current_user")
    user, = db_guest_cursor.fetchone()
    assert user == "app_guest"


@pytest.mark.parametrize("sql", [
    "SELECT * FROM users",
    "INSERT INTO users (first_name) VALUES ('hacker')",
    "UPDATE users SET first_name = 'bad' WHERE user_id = 1",
    "DELETE FROM users WHERE user_id = 1"
])
def test_reject_raw_table_access(db_guest_cursor, sql):
    with pytest.raises(errors.InsufficientPrivilege):
        db_guest_cursor.execute(sql)


@pytest.mark.parametrize("sql", [
    "SELECT * FROM utils.get_business_id_by_crn('12345678')",
    "SELECT * FROM utils.test_table",
])
def test_utils_schema_access_control(db_guest_cursor, sql):
    with pytest.raises(errors.InsufficientPrivilege):
        db_guest_cursor.execute(sql)