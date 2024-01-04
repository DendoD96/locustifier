from pydantic import BaseModel
from typing import Optional, List

from sample.models.locust_task import LocustTask


class LocustScenario(BaseModel):
    description: Optional[str]
    wait: int | List[int]
    host: str
    tasks: List[LocustTask]
