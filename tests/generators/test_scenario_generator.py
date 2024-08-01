import textwrap
import unittest

from black import FileMode, format_str
from locustifier.generators.scenario_generator import generate_scenario

from locustifier.models.locust_scenario import LocustScenario


class TestScenarioGenerator(unittest.TestCase):
    # Necessary to print multiline test description.
    def shortDescription(self):
        return None

    def test_locust_scenario_code_generation_with_tuple_wait(self):
        """
        Test the generation of Locust scenario code with a tuple for
        wait_time.
        """
        expected = """
            from locust import FastHttpUser, between
            from fake.module import UserScenario

            class UserScenario(FastHttpUser):
                host = \"http://localhost:8080\"
                tasks = [UserScenarioTasks]
                wait_time = between(2, 5)
                weight = 1
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
        generated_locust_scenario_code = generate_scenario(
            instance, "fake.module", "UserScenario"
        )
        self.assertEqual(
            generated_locust_scenario_code,
            format_str(textwrap.dedent(expected), mode=FileMode()),
        )

    def test_locust_scenario_code_generation_with_int_wait(self):
        """
        Test the generation of Locust scenario code with an int for
        wait_time.
        """
        expected = """
            from locust import FastHttpUser, between
            from fake.module import UserScenario

            class UserScenario(FastHttpUser):
                host = \"http://localhost:8080\"
                tasks = [UserScenarioTasks]
                wait_time = between(2, 2)
                weight = 1
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
        generated_locust_scenario_code = generate_scenario(
            instance, "fake.module", "UserScenario"
        )
        self.assertEqual(
            generated_locust_scenario_code,
            format_str(textwrap.dedent(expected), mode=FileMode()),
        )


if __name__ == "__main__":
    unittest.main()
