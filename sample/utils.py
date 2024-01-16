import re
from faker import Faker


fake = Faker()


def string_to_upper_camel_case(input_string: str) -> str:
    """
    Convert a string to Upper Camel Case.

    This function takes an input string and converts it to Upper Camel Case,
    where each word is capitalized and spaces or non-alphanumeric characters
    are removed.

    Parameters:
    - input_string (str): The input string to be converted.

    Returns:
    - str: The input string converted to Upper Camel Case.
    """
    cleaned_string = re.sub(r"[^a-zA-Z0-9]+", " ", input_string)
    camel_case_words = [word.capitalize() for word in cleaned_string.split()]
    return "".join(camel_case_words)


def string_to_snake_case(input_string: str) -> str:
    """
    Convert a string to Snake Case.

    This function takes an input string and converts it to Snake Case, where
    spaces or non-alphanumeric characters are replaced with underscores, and
    the entire string is converted to lowercase.

    Parameters:
    - input_string (str): The input string to be converted.

    Returns:
    - str: The input string converted to Snake Case.
    """
    cleaned_string = re.sub(r"[^a-zA-Z0-9]+", " ", input_string)
    return ("".join(cleaned_string)).lower().replace(" ", "_")
