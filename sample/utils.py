import re
from faker import Faker


fake = Faker()


def string_to_upper_camel_case(input_string: str) -> str:
    cleaned_string = re.sub(r"[^a-zA-Z0-9]+", " ", input_string)
    camel_case_words = [word.capitalize() for word in cleaned_string.split()]
    return "".join(camel_case_words)


def string_to_snake_case(input_string: str) -> str:
    cleaned_string = re.sub(r"[^a-zA-Z0-9]+", " ", input_string)
    return ("".join(cleaned_string)).lower().replace(" ", "_")
