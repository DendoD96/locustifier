from http import HTTPMethod
from typing import List, Optional
from pydantic import BaseModel, validator
from locustifier.models.fake_body_parameter import (
    FakeBodyParameter,
    ValueBodyParameter,
)
from locustifier.models.path_parameter import PathParameter


class LocustTask(BaseModel):
    """
    Pydantic model representing a Locust task with various properties.

    Attributes:
        name (str): The name of the Locust task.
        method (HTTPMethod): The HTTP method for the task (GET, POST, etc.).
        path (str): The URL path for the task.
        path_params (Optional[List[PathParameter]]): Optional list of \
            path parameters.
        query_params (Optional[dict]): Optional dictionary of query parameters.
        headers (Optional[dict]): Optional dictionary of headers.
        weight (Optional[int]): The weight assigned to the task for \
            task scheduling.
        req_body (Optional[List[FakeBodyParameter]]): Optional list of \
            fake body parameters.

    Raises:
        ValueError: If req_body is provided for unsupported HTTP methods \
            (GET, DELETE, etc.).
    """

    name: str
    method: HTTPMethod
    path: str
    path_params: Optional[List[PathParameter]] = None
    query_params: Optional[dict] = None
    headers: Optional[dict] = None
    weight: Optional[int] = 1
    req_body: Optional[List[FakeBodyParameter | ValueBodyParameter]] = None

    @validator("req_body", pre=True, always=True)
    def check_conditional_field(cls, value, values):
        method = values.get("method")

        if (
            method not in [HTTPMethod.POST, HTTPMethod.PATCH, HTTPMethod.PUT]
            and value is not None
        ):
            raise ValueError(
                f"{value} is not allowed when HTTP request method id {method}"
            )

        return value
