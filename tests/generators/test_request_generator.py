import re
import textwrap
import unittest

from black import FileMode, format_str
from sample.generators.request_generator import generate_request_code

from sample.models.locust_task import LocustTask


class TestRequestGenerator(unittest.TestCase):
    # Necessary to print multiline test description.
    def shortDescription(self):
        return None

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
        generated_request_code = generate_request_code(instance)
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
        generated_request_code = generate_request_code(instance)
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
