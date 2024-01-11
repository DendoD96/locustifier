from black import FileMode, format_str
from sample.models.locust_scenario import LocustScenario


SCENARIO_FILE_BASE_STRUCTURE = """
from locust import HttpUser, between
from {taskset_module} import {taskset_class}

{scenario_code}
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
    scenario_code = scenario.generate_scenario_code()
    format_str(
        SCENARIO_FILE_BASE_STRUCTURE.format(
            taskset_module=taskset_module,
            taskset_class=taskset_class,
            scenario_code=scenario_code,
        ),
        mode=FileMode(),
    )
