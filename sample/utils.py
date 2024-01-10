import re
from faker import Faker


fake = Faker()


def string_to_upper_camel_case(input_string: str) -> str:
    cleaned_name = re.sub(r"[^a-zA-Z0-9]+", " ", input_string)
    camel_case_words = [word.capitalize() for word in cleaned_name.split()]
    return "".join(camel_case_words)


def string_to_snake_case(input_string: str) -> str:
    return "_".join(
        re.sub(
            "([A-Z][a-z]+)",
            r" \1",
            re.sub("([A-Z]+)", r" \1", input_string.replace("-", " ")),
        ).split()
    ).lower()
