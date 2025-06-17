from . import db, db_errors


class Business:
    def __init__(self, token: str, crn_no: str) -> None:
        self.crn_no = crn_no
        self.user_token = token

    @classmethod
    def create_for_user(cls: "type[Business]", token: str, **details):
        db_errors.unwrap_result(db.proc_create_business(token, **details))
        return cls(token, details['crn_no'])

    def add_resource(self, quantity: int, resource_name: str) -> None:
        db_errors.unwrap_result(db.proc_add_business_resource(
            self.user_token, self.crn_no, resource_name, quantity
        ))


def exists_business(*, crn: str = "", vat: str = "", utr: str = "") -> bool:
    if crn:
        return db.proc_exists_business_crn(crn)
    if vat:
        return db.proc_exists_business_vat(vat)
    if utr:
        return db.proc_exists_business_utr(utr)
    raise RuntimeError("Unreachable code")