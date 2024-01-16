import uuid
from faker import Faker

BASIC_PROVIDER = {
    "int": "random_int",
    "float": "pyfloat",
    "bool": "pybool",
    "str": "word",
}
MAX_LIST_ELEM = 900

fake = Faker()


def generate_value(parameter_type: str, items: int, count: int, provider: str):
    """
    Generate a fake value based on the specified parameter.
    Returns:
        Any: The generated fake value.
    """

    def recursive_generate_value():
        if parameter_type == "uuid":
            return str(uuid.uuid4())
        if parameter_type in ["int", "float", "bool", "str"]:
            generator = getattr(
                fake,
                provider if provider else BASIC_PROVIDER[parameter_type],
                None,
            )
            return generator()
        return [recursive_generate_value(items) for _ in range(count)]

    return recursive_generate_value()
