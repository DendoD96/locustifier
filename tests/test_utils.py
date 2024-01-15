import unittest

from sample.utils import string_to_snake_case, string_to_upper_camel_case


class TestUtils(unittest.TestCase):
    # Necessary to print multiline test description.
    def shortDescription(self):
        return None

    def test_string_to_upper_camel_case(self):
        """
        Test string_to_upper_camel_case function.

        It should convert strings to upper camel case.
        """
        strings = [
            "Test upper",
            "test upper",
            "test-upper",
            "test_upper",
            "test@upper",
        ]
        upper_strings = [string_to_upper_camel_case(s) for s in strings]
        assert all(s == "TestUpper" for s in upper_strings)

    def test_string_to_snake_case(self):
        """
        Test string_to_snake_case function.

        It should convert strings to snake case.
        """
        strings = [
            "Test snake",
            "test snake",
            "test-snake",
            "test_snake",
            "test@snake",
        ]
        snake_strings = [string_to_snake_case(s) for s in strings]
        assert all(s == "test_snake" for s in snake_strings)
