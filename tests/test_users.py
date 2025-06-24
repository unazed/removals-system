import pytest

from removals_system.models import db

import logging

g_logger = logging.getLogger(__name__)


@pytest.mark.parametrize("phone_type", ["home", "work"])
def test_create_phone_number(db_guest_cursor, with_valid_user, phone_type):
    email, password, result = with_valid_user("customer")
    token = result.data.token

    phone_result = db.proc_create_user_phone_number(
        token,
        extension="+44",
        number=f"123456789",
        phone_type=phone_type,
    )

    assert phone_result.success, f"Should successfully add {phone_type} phone number"

    fetch_result = db.proc_get_user_phone_numbers(token)
    assert fetch_result.success
    assert any(pn.phone_number == f"123456789" and pn.phone_number_type == phone_type
               for pn in fetch_result.data)


@pytest.mark.parametrize("address_type", ["home", "office", "mailing"])
def test_create_user_address(db_guest_cursor, with_valid_user, address_type):
    email, password, result = with_valid_user("customer")
    token = result.data.token

    address_result = db.proc_create_user_address(
        token,
        line_1=f"123 {address_type.title()} Street",
        line_2="Suite 100",
        line_3="",
        city="Bedford",
        county="Bedfordshire",
        country="United Kingdom",
        post_code="SW1A 1AA",
        address_type=address_type,
    )

    assert address_result.success, f"Should successfully add {address_type} address"

    fetch_result = db.proc_get_user_addresses(token)
    assert fetch_result.success
    assert any(addr.line_1 == f"123 {address_type.title()} Street" and addr.address_type == address_type
               for addr in fetch_result.data)