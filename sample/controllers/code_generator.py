import json
import os
import shutil
from typing import List
from sample.generators.request_generator import generate_requests_code
from sample.generators.scenario_generator import generate_scenario

from sample.generators.taskset_generator import generate_taskset

from sample.models.locust_scenario import LocustScenario
from sample.utils import string_to_snake_case, string_to_upper_camel_case

STATIC_CODE_FOLDER = "static"
REQUEST_UTILS_FILE_NAME = "utils"
GENERATED_FOLDER = "generated"
REQUEST_FOLDER = os.path.join(GENERATED_FOLDER, "requests")
LOCUSTFILES_FOLDER = os.path.join(GENERATED_FOLDER, "locustfiles")
TASKS_FOLDER = os.path.join(LOCUSTFILES_FOLDER, "tasks")


class CodeGenerator:
    def __init__(self, json_specification_file_path) -> None:
        self.json_specification_file_path = json_specification_file_path

    def __generate_base_structure(self):
        # Create directories
        os.makedirs(REQUEST_FOLDER, exist_ok=True)
        os.makedirs(LOCUSTFILES_FOLDER, exist_ok=True)
        os.makedirs(TASKS_FOLDER, exist_ok=True)

        for folder in REQUEST_FOLDER, TASKS_FOLDER:
            # Create __init__.py files
            with open(os.path.join(folder, "__init__.py"), "w") as _:
                pass

    def __generate_requests(self, scenario: LocustScenario):
        scenario_name_snake_case: str = string_to_snake_case(scenario.name)
        with open(
            os.path.join(
                REQUEST_FOLDER,
                f"{scenario_name_snake_case}_requests.py",
            ),
            "w",
        ) as requests_file:
            requests_module = REQUEST_FOLDER.replace(os.path.sep, ".")
            requests_file.write(
                generate_requests_code(
                    request_utils_module=f"{requests_module}.\
                        {REQUEST_UTILS_FILE_NAME}",
                    taskset=scenario,
                )
            )

    def __generate_tasks(self, scenario: LocustScenario):
        scenario_name_snake_case: str = string_to_snake_case(scenario.name)
        requests_file: str = f"{scenario_name_snake_case}_requests"
        task_file_name: str = os.path.join(
            TASKS_FOLDER,
            f"{scenario_name_snake_case}_tasks.py",
        )
        taskset_name: str = f"{string_to_upper_camel_case(scenario.name)}Tasks"
        with open(task_file_name, "w") as tasks_file:
            tasks_file.write(
                generate_taskset(
                    taskset=scenario,
                    requests_module=REQUEST_FOLDER.replace(os.path.sep, "."),
                    requests_file=requests_file,
                    taskset_name=taskset_name,
                )
            )

    def ___generate_scenario(self, scenario: LocustScenario):
        scenario_name_snake_case = string_to_snake_case(scenario.name)
        tasks_file = f"{scenario_name_snake_case}_tasks"
        with open(
            os.path.join(
                LOCUSTFILES_FOLDER,
                f"{scenario_name_snake_case}.py",
            ),
            "w",
        ) as scenario_file:
            taskset_module = (
                f"{TASKS_FOLDER.replace(os.path.sep, '.')}.{tasks_file}"
            )
            taskset_class = f"{string_to_upper_camel_case(scenario.name)}Tasks"
            scenario_file.write(
                generate_scenario(
                    scenario=scenario,
                    taskset_class=taskset_class,
                    taskset_module=taskset_module,
                )
            )

    def generate(self):
        """
        Parse the JSON specifications file and generate the output files.

        Raises:
        - FileNotFoundError: If the specified JSON file does not exist.
        - PermissionError: If there is a permission error while
          trying to open the JSON file.
        - ValidationError: If the parsed JSON does not conform to
          the LocustScenario Pydantic model.
        """
        with open(self.json_specification_file_path, "r") as json_file_buffer:
            json_file_content: List[dict] = json.load(json_file_buffer)
            scenarios: List[LocustScenario] = [
                LocustScenario(**scenario) for scenario in json_file_content
            ]
            self.__generate_base_structure()
            shutil.copytree(
                STATIC_CODE_FOLDER, GENERATED_FOLDER, dirs_exist_ok=True
            )
            for scenario in scenarios:
                self.__generate_requests(scenario)
                self.__generate_tasks(scenario)
                self.___generate_scenario(scenario)
