import textwrap
import unittest

from black import FileMode, format_str
from sample.generators.task_generator import generate_locust_task_code

from sample.models.locust_task import LocustTask


class TestTaskGenerator(unittest.TestCase):
    # Necessary to print multiline test description.
    def shortDescription(self):
        return None

    def test_locust_task_code_generation(self):
        """
        Ensures that the generated Locust task code matches the expected
        format.
        """
        request_file = "requests"
        expected = f"""
            @task(1)
            def update_user(self):
                {request_file}.update_user(self.client)
        """
        data = {
            "name": "update_user",
            "method": "GET",
            "path": "/user/{id}",
            "path_params": [{"name": "id", "value": "123"}],
        }
        instance = LocustTask(**data)
        generated_locust_task_code = generate_locust_task_code(
            instance, request_file
        )
        self.assertEqual(
            generated_locust_task_code,
            format_str(textwrap.dedent(expected), mode=FileMode()),
        )
