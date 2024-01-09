import json
import os
from typing import List
from sample.models.locust_scenario import LocustScenario
from sample.models.locust_task import LocustTask

SCENARIO_IMPORTS = """
from locust import task, between, TaskSet
"""
GENERATED_FOLDER = "generated"
REQUEST_FOLDER = f"{GENERATED_FOLDER}/requests"
LOCUSTFILES_FOLDER = f"{GENERATED_FOLDER}/locustfiles"


class CodeGenerator:
    def __init__(self, json_specification_file_path) -> None:
        self.json_specification_file_path = json_specification_file_path

    def __generate_base_structure(self):
        # Create directories
        os.makedirs(REQUEST_FOLDER, exist_ok=True)
        os.makedirs(LOCUSTFILES_FOLDER, exist_ok=True)

        # Create __init__.py files
        with open(os.path.join(REQUEST_FOLDER, "__init__.py"), "w") as _:
            pass

    def __generate_requests(self, tasks: List[LocustTask]):
        requests = [task.generate_request_code() for task in tasks]
        print("\n".join(requests))

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
            print(scenarios)
            self.__generate_base_structure()
            for scenario in scenarios:
                self.__generate_requests(scenario.tasks)
