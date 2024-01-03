from enum import Enum
from typing import Literal
from pydantic import BaseModel


class PathParameterStyle(str, Enum):
    simple = "simple"
    label = "label"
    matrix = "matrix"


class PathParameter(BaseModel):
    name: str
    # TODO: can also be an object, but OpenAPI serialization
    # seems not working in connexion.
    value: int | float | bool | str | list
    style: Literal[
        "simple", "label", "matrix"
    ] = "simple"  # Default from OpenAPI spec
    explode: bool = False  # Default from OpenAPI spec
