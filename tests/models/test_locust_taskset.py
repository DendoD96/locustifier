import unittest

from locustifier.models.locust_task import LocustTask
from locustifier.models.locust_taskset import LocustTaskSet


class TestLocustTaskSet(unittest.TestCase):
    # Necessary to print multiline test description.
    def shortDescription(self):
        return None

    def test_simple_taskset_generation(self):
        """Test creating an instance of LocustTaskSet with valid input."""
        data = {
            "tasks": []
        }
        instance = LocustTaskSet(**data)

        # Assert that the instance is of MyModel
        self.assertIsInstance(instance, LocustTaskSet)

    def test_sequential_taskset_generation(self):
        """Test creating an instance of sequential LocustTaskSet."""
        data = {
            "is_sequential": True,
            "tasks": []
        }
        instance = LocustTaskSet(**data)
        self.assertTrue(instance.is_sequential)

    def test_taskset_task_generation(self):
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

        self.assertIsInstance(instance.tasks[0], LocustTask)
        self.assertEqual(len(instance.tasks), 2)

if __name__ == "__main__":
    unittest.main()
