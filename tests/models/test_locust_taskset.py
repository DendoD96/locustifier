import unittest

from sample.models.locust_task import LocustTask
from sample.models.locust_taskset import LocustTaskSet


class TestLocustTaskSet(unittest.TestCase):
    # Necessary to print multiline test description.
    def shortDescription(self):
        return None

    def test_simple_taskset_generation(self):
        """Test creating an instance of LocustTaskSet with valid input."""

        data = {
            "tasks": [
                {
                    "name": "get_user",
                    "method": "GET",
                    "path": "/users/{id}",
                    "path_params": [{"name": "id", "value": ""}],
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

        # Assert that the instance is of MyModel
        self.assertIsInstance(instance, LocustTaskSet)
        self.assertIsInstance(instance.tasks[0], LocustTask)

        # Assert that the values match the input data
        self.assertEqual(len(instance.tasks), 2)
