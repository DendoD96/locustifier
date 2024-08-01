import textwrap
import unittest

from black import FileMode, format_str
from locustifier.generators.taskset_generator import generate_taskset

from locustifier.models.locust_taskset import LocustTaskSet


def get_expected_stub(
    request_module: str,
    request_file: str,
    taskset_name: str,
    taskset_type: str,
) -> str:
    return f"""
        from {request_module} import {request_file}
        from locust import task, {taskset_type}


        class {taskset_name}({taskset_type}):
            @task(1)
            def get_user(self):
                requests.get_user(self.client)

            @task(1)
            def get_users(self):
                requests.get_users(self.client)
        """


class TestTasksetGenerator(unittest.TestCase):
    # Necessary to print multiline test description.
    def shortDescription(self):
        return None

    def test_locust_taskset_code_generation(self):
        """Ensures that the generated code matches the expected structure."""
        request_module = "request.module"
        request_file = "requests"
        taskset_name = "TaskSetName"
        data = {
            "tasks": [
                {
                    "name": "get_user",
                    "method": "GET",
                    "path": "/users/{id}",
                    "path_params": [
                        {
                            "name": "id",
                            "value": "0326dce2-b212-427c-aa18-811648fb6594",
                        }
                    ],
                    "query_params": {},
                    "headers": {},
                    "weight": 1,
                },
                {
                    "name": "get_users",
                    "method": "GET",
                    "path": "/users",
                    "weight": 1,
                },
            ]
        }
        instance = LocustTaskSet(**data)
        generated_locust_tasksset_code = generate_taskset(
            taskset=instance,
            requests_module=request_module,
            requests_file=request_file,
            taskset_name=taskset_name,
        )
        self.assertEqual(
            generated_locust_tasksset_code,
            format_str(
                textwrap.dedent(
                    get_expected_stub(
                        request_file=request_file,
                        request_module=request_module,
                        taskset_name=taskset_name,
                        taskset_type="TaskSet",
                    )
                ),
                mode=FileMode(),
            ),
        )

    def test_locust_sequentialtaskset_code_generation(self):
        """Ensures that the generated code matches the expected structure."""
        request_module = "request.module"
        request_file = "requests"
        taskset_name = "TaskSetName"
        data = {
            "tasks": [
                {
                    "name": "get_user",
                    "method": "GET",
                    "path": "/users/{id}",
                    "path_params": [
                        {
                            "name": "id",
                            "value": "0326dce2-b212-427c-aa18-811648fb6594",
                        }
                    ],
                    "query_params": {},
                    "headers": {},
                    "weight": 1,
                },
                {
                    "name": "get_users",
                    "method": "GET",
                    "path": "/users",
                    "weight": 1,
                },
            ],
            "is_sequential": True,
        }
        instance = LocustTaskSet(**data)
        generated_locust_tasksset_code = generate_taskset(
            taskset=instance,
            requests_module=request_module,
            requests_file=request_file,
            taskset_name=taskset_name,
        )
        self.assertEqual(
            generated_locust_tasksset_code,
            format_str(
                textwrap.dedent(
                    get_expected_stub(
                        request_file=request_file,
                        request_module=request_module,
                        taskset_name=taskset_name,
                        taskset_type="SequentialTaskSet",
                    )
                ),
                mode=FileMode(),
            ),
        )


if __name__ == "__main__":
    unittest.main()
