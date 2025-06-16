from .db import proc_get_type_values, proc_get_type_table_names

def get_type_values(type_name: str) -> list[str]:
    type_tables = proc_get_type_table_names()
    type_name = type_name.lower()
    if type_name not in type_tables:
        raise KeyError(f"No such type table: {type_name!r}")
    return proc_get_type_values(type_name)