import json
from jinja2 import Template
import yaml
import os
import shutil
from typing import List

from locustifier.generators.request_generator import generate_requests_code
from locustifier.generators.scenario_generator import generate_scenario

from locustifier.generators.taskset_generator import generate_taskset

from locustifier.models.locust_scenario import LocustScenario
from locustifier.utils import string_to_snake_case, string_to_upper_camel_case

STATIC_CODE_FOLDER = os.path.join(os.path.dirname(__file__), "static")
REQUEST_UTILS_FILE_NAME = "utils"
GENERATED_FOLDER = "generated"
REQUEST_FOLDER = os.path.join(GENERATED_FOLDER, "requests")
REQUEST_FILE_TEMPLATE = "{scenario_name_snake_case}_requests"
LOCUSTFILES_FOLDER = os.path.join(GENERATED_FOLDER, "locustfiles")
TASKS_FOLDER = os.path.join(LOCUSTFILES_FOLDER, "tasks")
TASKSET_CLASS_TEMPLATE = "{scenario_name_upper_camel_case}Tasks"
TASKSET_FILE_TEMPLATE = "{scenario_name_snake_case}_tasks"


class CodeGenerator:
    """
    A class for generating code based on JSON specifications.

    This class takes a JSON specifications file path, processes the content,
    and generates code files for Locust.

    Parameters:
    - specification_file_path (str): The path to the JSON
    specifications file.

    Methods:
    - generate: Parse the JSON specifications file and generate the
      output files.

    Private Methods:
    - __generate_base_structure: Generate the base directory structure and
      necessary __init__.py files.
    - __generate_requests: Generate Locust requests code for a given scenario.
    - __generate_tasks: Generate Locust task set code for a given scenario.
    - __generate_scenario: Generate Locust scenario code for a given scenario.
    - __get_requests_file_path: Get the file path for the requests file
      of a scenario.
    - __get_taskset_file_path: Get the file path for the task set file
      of a scenario.
    - __get_scenario_file_path: Get the file path for the scenario file
      of a scenario.
    - __write_file: Write content to a file.

    Note:
    The generated code files will be organized into specified
      folders and follow
    a naming convention based on the names of scenarios.
    """

    def __init__(self, specification_file_path) -> None:
        self.specification_file_path = specification_file_path

    @staticmethod
    def __generate_base_structure():
        # Create directories
        os.makedirs(REQUEST_FOLDER, exist_ok=True)
        os.makedirs(LOCUSTFILES_FOLDER, exist_ok=True)
        os.makedirs(TASKS_FOLDER, exist_ok=True)

        for folder in REQUEST_FOLDER, TASKS_FOLDER:
            # Create __init__.py files
            with open(os.path.join(folder, "__init__.py"), "w") as _:
                pass

    @staticmethod
    def __generate_requests(scenario: LocustScenario) -> str:
        requests_module = REQUEST_FOLDER.replace(os.path.sep, ".")
        return generate_requests_code(
            request_utils_module=f"{requests_module}.\
                        {REQUEST_UTILS_FILE_NAME}",
            taskset=scenario,
        )

    @staticmethod
    def __generate_tasks(scenario: LocustScenario) -> str:
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

    @staticmethod
    def ___generate_scenario(scenario: LocustScenario) -> str:
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

    @staticmethod
    def __get_requests_file_path(scenario_name_snake_case: str) -> str:
        request_file: str = REQUEST_FILE_TEMPLATE.format(
            scenario_name_snake_case=scenario_name_snake_case
        )
        return os.path.join(REQUEST_FOLDER, f"{request_file}.py")

    @staticmethod
    def __get_taskset_file_path(scenario_name_snake_case: str) -> str:
        taskset_file_name = TASKSET_FILE_TEMPLATE.format(
            scenario_name_snake_case=scenario_name_snake_case
        )

        return os.path.join(TASKS_FOLDER, f"{taskset_file_name}.py")

    @staticmethod
    def __get_scenario_file_path(scenario_name_snake_case: str) -> str:
        return os.path.join(
            LOCUSTFILES_FOLDER,
            f"{scenario_name_snake_case}.py",
        )

    @staticmethod
    def __write_file(file_name: str, file_content: str):
        with open(file_name, "w") as file:
            file.write(file_content)

    @staticmethod
    def __load_content(spec_file_path: str) -> List[dict]:
        with open(spec_file_path, "r") as file_buffer:
            content = file_buffer.read()
            template = Template(content)
            rendered_content = template.render()

            try:
                return json.loads(rendered_content)
            except json.JSONDecodeError:
                pass

            try:
                return yaml.safe_load(rendered_content)
            except yaml.YAMLError:
                pass

            raise ValueError()

    def generate(self):
        """Parse the JSON specifications file and generate the output files."""
        file_content: List[dict] = self.__load_content(
            self.specification_file_path
        )
        scenarios: List[LocustScenario] = [
            LocustScenario(**scenario) for scenario in file_content
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
