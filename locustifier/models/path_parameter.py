from enum import Enum
from typing import Literal, Optional
from pydantic import BaseModel


class PathParameterStyle(str, Enum):
    """
    Enumeration representing different styles for path parameters.

    This enumeration defines styles for path parameters, which can be used to
    specify how parameters should be included in a URL path.

    Enumeration Values:
    - `simple`: Parameters are included as part of the path as-is.
    - `label`: Parameters are included as path segments with a label.
    - `matrix`: Parameters are included in a matrix within the path.

    Example:
    ```python
    style = PathParameterStyle.label
    ```
    """

    simple = "simple"
    label = "label"
    matrix = "matrix"


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
