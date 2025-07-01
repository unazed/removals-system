from psycopg2 import errors
import pytest

from removals_system.models import db
from .conftest import gen_rand_alpha

import logging
import random
import string

g_logger = logging.getLogger(__name__)


def gen_rand_alpha(length: int) -> str:
    return ''.join(random.sample(string.ascii_letters, length))


def test_create_business(db_guest_cursor, with_valid_user):
    *_, session = with_valid_user("service-provider")
    db.proc_create_business(
        session.data.token,
        business_name="Sample business name",
        vat_no=gen_rand_alpha(length=11),
        crn_no=gen_rand_alpha(length=8),
        utr_no=gen_rand_alpha(length=10),
        num_employees=16
    )


@pytest.mark.parametrize("lengths", [
    [1, 8, 10, 2],
    [11, 1, 10, 2],
    [11, 8, 1, 2],
    [11, 8, 10, 0]
])
def test_invalid_business_params(db_guest_cursor, with_valid_user, lengths):
    *_, session = with_valid_user("service-provider")
    with pytest.raises(errors.CheckViolation):
        db.proc_create_business(
            session.data.token,
            business_name="Sample business name",
            vat_no=gen_rand_alpha(length=lengths[0]),
            crn_no=gen_rand_alpha(length=lengths[1]),
            utr_no=gen_rand_alpha(length=lengths[2]),
            num_employees=lengths[3]
        )


def test_appropriate_role_permission(db_guest_cursor, with_valid_user):
    *_, session = with_valid_user("customer")
    fetch_result = db.proc_create_business(
        session.data.token,
        business_name="Sample business name",
        vat_no=gen_rand_alpha(length=11),
        crn_no=gen_rand_alpha(length=8),
        utr_no=gen_rand_alpha(length=10),
        num_employees=2
    )
    g_logger.info(fetch_result)
    assert not fetch_result.success


def test_create_business_resource(db_guest_cursor, with_valid_business):
    *_, session, crn_no = with_valid_business
    db.proc_add_business_resource(
        session.data.token,
        crn_no,
        "storage unit",
        16
    )