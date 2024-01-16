import uuid
from faker import Faker

BASIC_PROVIDER = {
    "int": "random_int",
    "float": "pyfloat",
    "bool": "pybool",
    "str": "word",
}

fake = Faker()


def generate_value(
    parameter_type: str,
    items: dict | None = None,
    count: int = None,
    provider: str | None = None,
):
    """
    Generate a fake value based on the specified parameter.
    Returns:
        Any: The generated fake value.
    """

    def recursive_generate_value(parameter_type: str, items: dict | None):
        if parameter_type == "uuid":
            return str(uuid.uuid4())
        if parameter_type in ["int", "float", "bool", "str"]:
            generator = getattr(
                fake,
                provider if provider else BASIC_PROVIDER[parameter_type],
                None,
            )
            return generator()
        return [
            recursive_generate_value(
                parameter_type=items["parameter_type"],
                items=items.get("items", None),
            )
            for _ in range(count)
        ]

    return recursive_generate_value(parameter_type, items)
