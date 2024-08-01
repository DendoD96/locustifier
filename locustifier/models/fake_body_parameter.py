from typing import Optional, Literal, Union
from pydantic import BaseModel, Field, validator

MAX_LIST_ELEM = 900


class BaseParameter(BaseModel):
    """
    Pydantic model representing a base parameter for request bodies.

    Attributes:
        parameter_type (Literal["int", "float", "bool", "str", "list"]): \
            The parameter_type of the parameter.
        count (int): The number of items (used for lists).
        items (Optional[BaseParameter]): Nested parameter for lists.
    """

    parameter_type: Literal["int", "float", "bool", "str", "list", "uuid"]
    count: int = Field(default=10, lt=MAX_LIST_ELEM)
    items: Optional["BaseParameter"] = None

    @validator("items", pre=True, always=True)
    def check_conditional_field(cls, value, values):
        parameter_type = values.get("parameter_type")

        if parameter_type == "list" and value is None:
            raise ValueError(
                f"{value} is required when parameter_type is a list"
            )

        return value


class FakeBodyParameter(BaseParameter):
    """
    Pydantic model representing a fake parameter for request bodies.

    Attributes:
        name (str): The name of the parameter.
        provider (Optional[str]): The custom provider for generating\
              fake values.
    """

    name: str
    provider: Optional[str] = None


class ValueBodyParameter(BaseParameter):
    """
    Pydantic model representing a user input value parameter
    for request bodies.

    Attributes:
        value (Union[int, float, bool, str, List]): The user input value.
    """

    value: Union[int, float, bool, str]

    @validator("value")
    def validate_value(cls, value, values):
        parameter_type = values.get("parameter_type")

        if parameter_type == "int" and not isinstance(value, int):
            raise ValueError(
                "Value must be an int when parameter_type is 'int'"
            )
        elif parameter_type == "float" and not isinstance(value, float):
            raise ValueError(
                "Value must be a float when parameter_type is 'float'"
            )
        elif parameter_type == "bool" and not isinstance(value, bool):
            raise ValueError(
                "Value must be a bool when parameter_type is 'bool'"
            )
        elif parameter_type == "str" and not isinstance(value, str):
            raise ValueError(
                "Value must be a str when parameter_type is 'str'"
            )
        elif parameter_type == "list":
            raise ValueError("Not supported list input value")
        return value
