from http import HTTPMethod
import textwrap
from typing import List, Optional
from pydantic import BaseModel, validator
from sample.models.fake_body_parameter import FakeBodyParameter

from sample.models.path_parameter import PathParameter

REQUEST_CODE_TEMPLATE = """
def {function_name}(client):
    client.request(
        method='{method}',
        url='{url}',
        {optional_headers},
        {optional_query_params},
        {optional_req_body},
    )
"""

LOCUST_TASK_CODE_TEMPLATE = """
@task({weight})
def {task_name}(self):
    requests.{task_name}(self)
"""


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

    def __get_request_path(self) -> str:
        if self.path_params:
            return self.path.format(
                **{param.name: param.value for param in self.path_params}
            )
        return self.path

    def __get_optional_parameter(self) -> dict:
        optional_parameters = {}

        if self.headers:
            optional_parameters["optional_headers"] = f"headers={self.headers}"
        if self.query_params:
            optional_parameters[
                "optional_query_params"
            ] = f"params={self.query_params}"
        if self.req_body:
            body_parameter_dict = {
                param.name: param.generate_value() for param in self.req_body
            }
            optional_parameters[
                "optional_req_body"
            ] = f"json={body_parameter_dict}"

        return optional_parameters

    def generate_request_code(self):
        return textwrap.dedent(
            REQUEST_CODE_TEMPLATE.format(
                function_name=self.name,
                method=self.method,
                url=self.__get_request_path(),
                **self.__get_optional_parameter(),
            )
        )

    def generate_locust_task_code(self):
        return textwrap.dedent(
            LOCUST_TASK_CODE_TEMPLATE.format(
                weight=self.weight, task_name=self.name
            )
        )
