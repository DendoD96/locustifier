from typing import List
from pydantic import BaseModel

from sample.models.locust_task import LocustTask


class LocustTaskSet(BaseModel):
    """
    Pydantic model representing a set of Locust tasks.

    Attributes:
        tasks (List[LocustTask]): The list of Locust tasks in the set.

    Note:
        This class is intended to be used as a base class for defining sets \
            of Locust tasks.
    """

    tasks: List[LocustTask]
