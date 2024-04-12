from typing import Optional, List

from locustifier.models.locust_taskset import LocustTaskSet


class LocustScenario(LocustTaskSet):
    """
    Pydantic model representing a Locust scenario with additional properties.

    Attributes:
        name (str): The name of the Locust scenario.
        description (Optional[str]): An optional description for the scenario.
        wait (int | List[int]): The wait time or a list representing a range.
        host (str): The host URL for the scenario.
    """

    name: str
    description: Optional[str]
    wait: int | List[int]
    host: Optional[str]
