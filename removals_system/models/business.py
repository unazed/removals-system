from . import db, db_errors


class Business:
    def __init__(self, token: str, crn_no: str) -> None:
        self.crn_no = crn_no
        self.user_token = token
        print(f"Business CRN: {self.crn_no}")

    @classmethod
    def create_for_user(cls: "type[Business]", token: str, **details):
        db_errors.unwrap_result(db.proc_create_business(token, **details))
        return cls(token, details['crn_no'])

    def add_resource(self, quantity: int, resource_name: str) -> None:
        db_errors.unwrap_result(db.proc_add_business_resource(
            self.user_token, self.crn_no, resource_name, quantity
        ))