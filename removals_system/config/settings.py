DB_CONFIG = {
    "host": "localhost",
    "dbname": "removals",
    "user": "app_guest",
    "password": "app_guest"
}


def update_config(**kwargs) -> None:
    DB_CONFIG.update(kwargs)