import re
import textwrap
from pydantic import BaseModel
from typing import Optional, List

from sample.models.locust_task import LocustTask

SCENARIO_CODE_TEMPLATE = """
class {scenario_name}(HttpUser):
    host = {host}
    tasks = [{task_class}]
    wait_time = between({min_wait}, {max_wait})
"""


class LocustScenario(BaseModel):
    name: str
    description: Optional[str]
    wait: int | List[int]
    host: str
    tasks: List[LocustTask]

    def __name_to_upper_camel_case(self):
        cleaned_name = re.sub(r"[^a-zA-Z0-9]+", " ", self.name)
        camel_case_words = [word.capitalize() for word in cleaned_name.split()]
        return "".join(camel_case_words)

    def generate_scenario_code(self):
        scenario_name = self.__name_to_upper_camel_case()
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
