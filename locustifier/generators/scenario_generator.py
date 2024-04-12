from black import FileMode, format_str
from locustifier.models.locust_scenario import LocustScenario
from locustifier.utils import string_to_upper_camel_case


SCENARIO_FILE_BASE_STRUCTURE = """
from locust import HttpUser, between
from {taskset_module} import {taskset_class}

class {scenario_name}(HttpUser):
    host = '{host}'
    tasks = [{task_class}]
    wait_time = between({min_wait}, {max_wait})
"""


def generate_scenario(
    scenario: LocustScenario, taskset_module: str, taskset_class: str
) -> str:
    """
    Generate a Locust scenario code.

    Args:
        scenario (LocustScenario): The Locust scenario to be generated.
        taskset_module (str): The name of the module containing \
            the Locust task set.
        taskset_class (str): The name of the Locust task set class.

    Returns:
        str: The generated Locust scenario code.
    """
    scenario_name = string_to_upper_camel_case(scenario.name)

    return format_str(
        SCENARIO_FILE_BASE_STRUCTURE.format(
            taskset_module=taskset_module,
            taskset_class=taskset_class,
            scenario_name=scenario_name,
            host=scenario.host,
            task_class=f"{scenario_name}Tasks",
            min_wait=(
                scenario.wait
                if isinstance(scenario.wait, int)
                else scenario.wait[0]
            ),
            max_wait=(
                scenario.wait
                if isinstance(scenario.wait, int)
                else scenario.wait[1]
            ),
        ),
        mode=FileMode(),
    )
