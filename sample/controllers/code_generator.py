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
REQUEST_FILE_TEMPLATE = "{scenario_name_snake_case}_requests"
LOCUSTFILES_FOLDER = os.path.join(GENERATED_FOLDER, "locustfiles")
TASKS_FOLDER = os.path.join(LOCUSTFILES_FOLDER, "tasks")
TASKSET_CLASS_TEMPLATE = "{scenario_name_upper_camel_case}Tasks"
TASKSET_FILE_TEMPLATE = "{scenario_name_snake_case}_tasks"


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

    def __generate_requests(self, scenario: LocustScenario) -> str:
        requests_module = REQUEST_FOLDER.replace(os.path.sep, ".")
        return generate_requests_code(
            request_utils_module=f"{requests_module}.\
                        {REQUEST_UTILS_FILE_NAME}",
            taskset=scenario,
        )

    def __generate_tasks(self, scenario: LocustScenario) -> str:
        scenario_name_snake_case: str = string_to_snake_case(scenario.name)
        requests_file: str = REQUEST_FILE_TEMPLATE.format(
            scenario_name_snake_case=scenario_name_snake_case
        )
        taskset_name: str = TASKSET_CLASS_TEMPLATE.format(
            scenario_name_upper_camel_case=string_to_upper_camel_case(
                scenario.name
            )
        )
        return generate_taskset(
            taskset=scenario,
            requests_module=REQUEST_FOLDER.replace(os.path.sep, "."),
            requests_file=requests_file,
            taskset_name=taskset_name,
        )

    def ___generate_scenario(self, scenario: LocustScenario) -> str:
        scenario_name_snake_case = string_to_snake_case(scenario.name)
        tasks_file = TASKSET_FILE_TEMPLATE.format(
            scenario_name_snake_case=scenario_name_snake_case
        )
        taskset_module = (
            f"{TASKS_FOLDER.replace(os.path.sep, '.')}.{tasks_file}"
        )
        taskset_class = TASKSET_CLASS_TEMPLATE.format(
            scenario_name_upper_camel_case=string_to_upper_camel_case(
                scenario.name
            )
        )
        return generate_scenario(
            scenario=scenario,
            taskset_class=taskset_class,
            taskset_module=taskset_module,
        )

    def __get_requests_file_path(self, scenario_name_snake_case: str) -> str:
        request_file: str = REQUEST_FILE_TEMPLATE.format(
            scenario_name_snake_case=scenario_name_snake_case
        )
        return os.path.join(REQUEST_FOLDER, f"{request_file}.py")

    def __get_taskset_file_path(self, scenario_name_snake_case: str) -> str:
        taskset_file_name = TASKSET_FILE_TEMPLATE.format(
            scenario_name_snake_case=scenario_name_snake_case
        )

        return os.path.join(TASKS_FOLDER, f"{taskset_file_name}.py")

    def __get_scenario_file_path(self, scenario_name_snake_case: str) -> str:
        return os.path.join(
            LOCUSTFILES_FOLDER,
            f"{scenario_name_snake_case}.py",
        )

    def __write_file(self, file_name: str, file_content: str):
        with open(file_name, "w") as file:
            file.write(file_content)

    def generate(self):
        """Parse the JSON specifications file and generate the output files."""

        with open(self.json_specification_file_path, "r") as json_file_buffer:
            json_file_content: List[dict] = json.load(json_file_buffer)
            scenarios: List[LocustScenario] = [
                LocustScenario(**scenario) for scenario in json_file_content
            ]
            self.__generate_base_structure()
            shutil.copytree(
                STATIC_CODE_FOLDER, GENERATED_FOLDER, dirs_exist_ok=True
            )
            file_name_to_content = {}
            for scenario in scenarios:
                scenario_name_snake_case = string_to_snake_case(scenario.name)
                file_name_to_content[
                    self.__get_requests_file_path(scenario_name_snake_case)
                ] = self.__generate_requests(scenario)
                file_name_to_content[
                    self.__get_taskset_file_path(scenario_name_snake_case)
                ] = self.__generate_tasks(scenario)
                file_name_to_content[
                    self.__get_scenario_file_path(scenario_name_snake_case)
                ] = self.___generate_scenario(scenario)

            for file_name, file_content in file_name_to_content.items():
                self.__write_file(file_name, file_content)
