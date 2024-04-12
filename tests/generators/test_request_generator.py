import textwrap
import unittest

from black import FileMode, format_str
from locustifier.generators.request_generator import generate_requests_code

from locustifier.models.locust_taskset import LocustTaskSet


class TestRequestGenerator(unittest.TestCase):
    # Necessary to print multiline test description.
    def shortDescription(self):
        return None

    def test_request_code_generation_with_path_parameters(self):
        """
        Ensures that the generated request code matches the expected format.
        The request path contains path_params.
        """
        expected = """
        from fake.module import generate_value

        def update_user(client):
            client.request(
                method="PUT",
                url="/user/123",
                headers={"accept": "application/json"},
                params={"fake_query_param": "fake"},
                json={"name": generate_value("str", None, 10, None)},
            )
        """

        data = {
            "tasks": [
                {
                    "name": "update_user",
                    "method": "PUT",
                    "path": "/user/{id}",
                    "path_params": [{"name": "id", "value": "123"}],
                    "headers": {"accept": "application/json"},
                    "query_params": {"fake_query_param": "fake"},
                    "req_body": [{"name": "name", "parameter_type": "str"}],
                }
            ]
        }
        instance = LocustTaskSet(**data)
        generated_request_code = generate_requests_code(
            "fake.module", instance
        )
        self.assertEqual(
            generated_request_code,
            format_str(
                textwrap.dedent(expected),
                mode=FileMode(),
            ),
        )

    def test_request_code_generation_without_path_parameters(self):
        """
        Ensures that the generated request code matches the expected
        format.
        """
        expected = """
            from fake.module import generate_value

            def update_user(client):
                client.request(
                    method="POST",
                    url="/user",
                    headers={"accept": "application/json"},
                    params={"fake_query_param": "fake"},
                    json={"name": generate_value("str", None, 10, None)},
                )
        """
        data = {
            "tasks": [
                {
                    "name": "update_user",
                    "method": "POST",
                    "path": "/user",
                    "headers": {"accept": "application/json"},
                    "query_params": {"fake_query_param": "fake"},
                    "req_body": [{"name": "name", "parameter_type": "str"}],
                }
            ]
        }
        instance = LocustTaskSet(**data)
        generated_request_code = generate_requests_code(
            "fake.module", instance
        )
        self.assertEqual(
            generated_request_code,
            format_str(
                textwrap.dedent(expected),
                mode=FileMode(),
            ),
        )


if __name__ == "__main__":
    unittest.main()
