import textwrap
import unittest
from sample.models.locust_scenario import LocustScenario


class TestLocustScenario(unittest.TestCase):
    # Necessary to print multiline test description.
    def shortDescription(self):
        return None

    def test_simple_scenario_generation(self):
        """Test creating an instance of LocustScenario with valid input."""

        data = {
            "name": "user scenario",
            "description": """This scenario is created to test user
            microservice""",
            "host": "http://localhost:8080",
            "wait": [2, 5],
            "tasks": [{"name": "fake", "method": "GET", "path": "/fake"}],
        }

        instance = LocustScenario(**data)

        # Assert that the instance is of MyModel
        self.assertIsInstance(instance, LocustScenario)

        # Assert that the values match the input data
        self.assertEqual(instance.description, data["description"])
        self.assertEqual(instance.host, data["host"])
        self.assertEqual(instance.wait, data["wait"])
        self.assertEqual(len(instance.tasks), 1)

    def test_locust_scenario_code_generation_with_tuple_wait(self):
        """
        Test the generation of Locust scenario code with a tuple for wait_time.
        """
        expected = """
            class UserScenario(HttpUser):
                host = http://localhost:8080
                tasks = [UserScenarioTasks]
                wait_time = between(2, 5)
        """
        data = {
            "name": "user scenario",
            "description": """This scenario is created to test user
            microservice""",
            "host": "http://localhost:8080",
            "wait": [2, 5],
            "tasks": [{"name": "fake", "method": "GET", "path": "/fake"}],
        }

        instance = LocustScenario(**data)
        generated_locust_scenario_code = instance.generate_scenario_code()
        self.assertEqual(
            generated_locust_scenario_code,
            textwrap.dedent(expected),
        )

    def test_locust_scenario_code_generation_with_int_wait(self):
        """
        Test the generation of Locust scenario code with an int for wait_time.
        """
        expected = """
            class UserScenario(HttpUser):
                host = http://localhost:8080
                tasks = [UserScenarioTasks]
                wait_time = between(2, 2)
        """
        data = {
            "name": "user scenario",
            "description": """This scenario is created to test user
            microservice""",
            "host": "http://localhost:8080",
            "wait": 2,
            "tasks": [{"name": "fake", "method": "GET", "path": "/fake"}],
        }

        instance = LocustScenario(**data)
        generated_locust_scenario_code = instance.generate_scenario_code()
        self.assertEqual(
            generated_locust_scenario_code,
            textwrap.dedent(expected),
        )
