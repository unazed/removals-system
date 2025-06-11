import phonenumbers


def is_valid_number(number: str) -> bool:
    try:
        result = phonenumbers.parse(number)
    except phonenumbers.NumberParseException:
        return False
    return (
        phonenumbers.is_possible_number(result)
        and phonenumbers.is_valid_number(result)
    )


def get_country_code(country_code: str) -> str:
    return str(phonenumbers.country_code_for_valid_region(country_code))


def extract_phone_components(number: str) -> tuple[str, str]:
    result = phonenumbers.parse(number)
    return (result.country_code, result.national_number)