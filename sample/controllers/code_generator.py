import json
import os
import textwrap
from typing import List

from black import FileMode, format_str

from sample.models.locust_scenario import LocustScenario
from sample.models.locust_task import LocustTask
from sample.utils import string_to_snake_case, string_to_upper_camel_case

SCENARIO_IMPORTS = """
from locust import task, between, TaskSet
"""
GENERATED_FOLDER = "generated"
REQUEST_FOLDER = os.path.join(GENERATED_FOLDER, "requests")
LOCUSTFILES_FOLDER = os.path.join(GENERATED_FOLDER, "locustfiles")
TASKS_FOLDER = os.path.join(LOCUSTFILES_FOLDER, "tasks")
TASK_FILE_BASE_STRUCTURE = f"""
from {REQUEST_FOLDER.replace(os.path.sep, ".")} import {{requests_file}}
from locust import task, TaskSet


class {{task_set_name}}(TaskSet):
{{task_list}}
"""
SCENARIO_FILE_BASE_STRUCTURE = """
from locust import HttpUser, between
from {tasks_file} import {tasks_class}

{scenario_code}
"""


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

    def __generate_requests(self, scenario_name: str, tasks: List[LocustTask]):
        requests = [task.generate_request_code() for task in tasks]
        with open(
            os.path.join(
                REQUEST_FOLDER,
                f"{scenario_name}_requests.py",
            ),
            "w",
        ) as requests_file:
            requests_file.write(
                "\n\n".join(requests),
            )

    def __generate_tasks(self, scenario_name: str, tasks: List[LocustTask]):
        scenario_name_snake_case = string_to_snake_case(scenario_name)
        requests_file = f"{scenario_name_snake_case}_requests"
        tasks = [
            task.generate_locust_task_code(requests_file) for task in tasks
        ]
        with open(
            os.path.join(
                TASKS_FOLDER,
                f"{scenario_name_snake_case}_tasks.py",
            ),
            "w",
        ) as tasks_file:
            tasks_file.write(
                format_str(
                    TASK_FILE_BASE_STRUCTURE.format(
                        task_set_name=f"\
                            {string_to_upper_camel_case(scenario_name)}Tasks",
                        requests_file=requests_file,
                        task_list=textwrap.indent("\n".join(tasks), "    "),
                    ),
                    mode=FileMode(),
                )
            )

    def ___generate_scenario(self, scenario: LocustScenario):
        scenario_name_snake_case = string_to_snake_case(scenario.name)
        tasks_file = f"{scenario_name_snake_case}_tasks"
        scenario_code = scenario.generate_scenario_code()
        with open(
            os.path.join(
                LOCUSTFILES_FOLDER,
                f"{scenario_name_snake_case}.py",
            ),
            "w",
        ) as scenario_file:
            scenario_file.write(
                format_str(
                    SCENARIO_FILE_BASE_STRUCTURE.format(
                        tasks_file=f"\
                            {TASKS_FOLDER.replace(os.path.sep, '.')}.\
                                {tasks_file}",
                        tasks_class=f"\
                            {string_to_upper_camel_case(scenario.name)}Tasks",
                        scenario_code=scenario_code,
                    ),
                    mode=FileMode(),
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
            for scenario in scenarios:
                snake_case_scenario_name = string_to_snake_case(scenario.name)
                self.__generate_requests(
                    snake_case_scenario_name, scenario.tasks
                )
                self.__generate_tasks(scenario.name, scenario.tasks)
                self.___generate_scenario(scenario)
