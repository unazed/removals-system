from . import db


class Business:
    def __init__(self, crn_no: str) -> None:
        self.crn_no = crn_no


def create_business_for_user(token: str, **details) -> Business:
    error = db.proc_create_business(token, **details)