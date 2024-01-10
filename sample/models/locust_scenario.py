import textwrap
from pydantic import BaseModel
from typing import Optional, List

from sample.models.locust_task import LocustTask
from sample.utils import string_to_upper_camel_case

SCENARIO_CODE_TEMPLATE = """
class {scenario_name}(HttpUser):
    host = '{host}'
    tasks = [{task_class}]
    wait_time = between({min_wait}, {max_wait})
"""


class LocustScenario(BaseModel):
    name: str
    description: Optional[str]
    wait: int | List[int]
    host: str
    tasks: List[LocustTask]

    def generate_scenario_code(self):
        scenario_name = string_to_upper_camel_case(self.name)
        return textwrap.dedent(
            SCENARIO_CODE_TEMPLATE.format(
                scenario_name=scenario_name,
                host=self.host,
                task_class=f"{scenario_name}Tasks",
                min_wait=self.wait
                if isinstance(self.wait, int)
                else self.wait[0],
                max_wait=self.wait
                if isinstance(self.wait, int)
                else self.wait[1],
            )
        )
