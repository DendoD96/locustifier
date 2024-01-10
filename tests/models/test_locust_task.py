import re
import textwrap
import unittest
from pydantic import ValidationError
from black import FileMode, format_str
from sample.models.locust_task import LocustTask


class TestLocustTask(unittest.TestCase):
    # Necessary to print multiline test description.
    def shortDescription(self):
        return None

    def test_request_body_not_allowed(self):
        """
        Test that creating a LocustTask with a request body incompatible with
        the http method (method different from POST, PUT, PATCH)
        raises a ValidationError.
        """
        data = {
            "name": "fake",
            "method": "GET",
            "path": "/fake",
            "req_body": {"name": "fake_argument", "type": "int"},
        }
        with self.assertRaises(ValidationError):
            LocustTask(**data)

    def test_simple_task_generation(self):
        """Test creating an instance of LocustTask with valid input."""

        data = {"name": "fake", "method": "GET", "path": "/fake"}

        instance = LocustTask(**data)

        # Assert that the instance is of MyModel
        self.assertIsInstance(instance, LocustTask)

        # Assert that the values match the input data
        self.assertEqual(instance.name, data["name"])
        self.assertEqual(instance.method, data["method"])
        self.assertEqual(instance.path, data["path"])

    def test_request_code_generation_with_path_parameters(self):
        """
        Ensures that the generated request code matches the expected format.
        The request path contains path_params.
        """

        expected = f"""
        def update_user(client):
            {(
                "client.request(method='PUT', url='/user/123', "
                "headers={{'accept': 'application/json'}}, "
                "params={{'fake_query_param': 'fake'}}, "
                "json={{'name': '{generated_name}'}})"
            )}"""

        data = {
            "name": "update_user",
            "method": "PUT",
            "path": "/user/{id}",
            "path_params": [{"name": "id", "value": "123"}],
            "headers": {"accept": "application/json"},
            "query_params": {"fake_query_param": "fake"},
            "req_body": [{"name": "name", "type": "str"}],
        }
        instance = LocustTask(**data)
        generated_request_code = instance.generate_request_code()
        self.assertEqual(
            generated_request_code,
            format_str(
                textwrap.dedent(
                    expected.format(
                        generated_name=re.search(
                            r'json={"name": "([a-zA-Z]+)"}',
                            generated_request_code,
                        ).group(1)
                    )
                ),
                mode=FileMode(),
            ),
        )

    def test_request_code_generation_without_path_parameters(self):
        """
        Ensures that the generated request code matches the expected format.
        """
        expected = f"""
        def update_user(client):
            {(
                "client.request(method='POST', url='/user', "
                "headers={{'accept': 'application/json'}}, "
                "params={{'fake_query_param': 'fake'}}, "
                "json={{'name': '{generated_name}'}})"
            )}
        """
        data = {
            "name": "update_user",
            "method": "POST",
            "path": "/user",
            "headers": {"accept": "application/json"},
            "query_params": {"fake_query_param": "fake"},
            "req_body": [{"name": "name", "type": "str"}],
        }
        instance = LocustTask(**data)
        generated_request_code = instance.generate_request_code()
        self.assertEqual(
            generated_request_code,
            format_str(
                textwrap.dedent(
                    expected.format(
                        generated_name=re.search(
                            r'json={"name": "([a-zA-Z]+)"}',
                            generated_request_code,
                        ).group(1)
                    )
                ),
                mode=FileMode(),
            ),
        )

    def test_locust_task_code_generation(self):
        """
        Ensures that the generated Locust task codematches the expected
        format.
        """
        request_file = "requests"
        expected = f"""
            @task(1)
            def update_user(self):
                {request_file}.update_user(self)
        """
        data = {
            "name": "update_user",
            "method": "GET",
            "path": "/user/{id}",
            "path_params": [{"name": "id", "value": "123"}],
        }
        instance = LocustTask(**data)
        generated_locust_task_code = instance.generate_locust_task_code(
            request_file
        )
        self.assertEqual(
            generated_locust_task_code,
            format_str(textwrap.dedent(expected), mode=FileMode()),
        )
