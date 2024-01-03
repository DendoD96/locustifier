from http import HTTPMethod
from typing import List, Optional
from pydantic import BaseModel, validator
from sample.models.fake_body_parameter import FakeBodyParameter

from sample.models.path_parameter import PathParameter


class LocustTask(BaseModel):
    name: str
    method: HTTPMethod
    path: str
    path_params: Optional[List[PathParameter]] = None
    query_params: Optional[dict] = None
    headers: Optional[dict] = None
    weight: Optional[int] = 1
    req_body: Optional[List[FakeBodyParameter]] = None

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
