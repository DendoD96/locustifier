from enum import Enum
from typing import Literal, Optional
from pydantic import BaseModel

class PathParameter(BaseModel):
    """
    Pydantic model representing a path parameter in a URL.

    Attributes:
        name (str): The name of the path parameter.
        value (Union[int, float, bool, str, list]): The value of the path \
            parameter.
        style (Optional[Literal["simple", "label", "matrix"]]): The style of \
            the path parameter.
            Default is "simple" as per the OpenAPI specification.
        explode (Optional[bool]): Whether the path parameter should be \
            exploded.
            Default is False as per the OpenAPI specification.

    Note:
        This class represents a path parameter in a URL, adhering to OpenAPI \
            specifications.
    """

    name: str
    value: int | float | bool | str | list
    style: Optional[
        Literal["simple", "label", "matrix"]
    ] = "simple"  # Default from OpenAPI spec
    explode: Optional[bool] = False  # Default from OpenAPI spec
