from ast import List
import http
from pydantic import BaseModel

from sample.models.path_parameter import PathParameter


class LocustTask(BaseModel):
    name: str
    method: http.HTTPMethod
    path: str
    path_params: List[PathParameter]
    query_params: dict
    headers: dict
    weight: int
