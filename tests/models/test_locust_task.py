import unittest
from pydantic import ValidationError
from locustifier.models.locust_task import LocustTask


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
            "req_body": {"name": "fake_argument", "parameter_type": "int"},
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


if __name__ == "__main__":
    unittest.main()
