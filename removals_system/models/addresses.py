from . import db


def get_countries() -> list[str]:
    return db.proc_get_countries()

def get_counties(country_name: str) -> list[str]:
    return [lst[0] for lst in db.proc_get_counties(country_name)]

def get_cities(country_name: str, county_name: str) -> list[str]:
    return [lst[0] for lst in db.proc_get_cities(country_name, county_name)]