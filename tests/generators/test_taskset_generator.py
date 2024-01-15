import textwrap
import unittest

from black import FileMode, format_str
from sample.generators.taskset_generator import generate_taskset

from sample.models.locust_taskset import LocustTaskSet


class TestTasksetGenerator(unittest.TestCase):
    # Necessary to print multiline test description.
    def shortDescription(self):
        return None

    def test_locust_taskset_code_generation(self):
        request_module = "request.module"
        request_file = "requests"
        taskset_name = "TaskSetName"
        expected = f"""
        from {request_module} import {request_file}
        from locust import task, TaskSet


        class {taskset_name}(TaskSet):
            @task(1)
            def get_user(self):
                requests.get_user(self.client)

            @task(1)
            def get_users(self):
                requests.get_users(self.client)
        """
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
                textwrap.dedent(expected),
                mode=FileMode(),
            ),
        )
