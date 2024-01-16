import unittest

from pydantic import ValidationError

from sample.models.fake_body_parameter import FakeBodyParameter


class TestFakeBodyParameter(unittest.TestCase):
    # Necessary to print multiline test description.
    def shortDescription(self):
        return None

    def test_invalid_body_parameter_value(self):
        """
        Test that creating a FakeBodyParameter with an invalid 'value'
        parameter raises a ValidationError.
        """
        data = {"name": "fake_argument", "parameter_type": "mycustomfaketype"}

        with self.assertRaises(ValidationError):
            FakeBodyParameter(**data)

    def test_valid_primitive_body_parameter(self):
        """
        Test that creating a FakeBodyParameter with a valid primitive 'value'
        does not raise any exceptions.
        """
        try:
            data = {"name": "fake_argument", "parameter_type": "int"}
            self.assertIsInstance(
                FakeBodyParameter(**data),
                FakeBodyParameter,
            )
        except Exception as e:
            self.fail(f"Unexpected exception raised: {e}")

    def test_missing_items_for_list_parameter(self):
        """
        Test that creating a FakeBodyParameter instance with missing items
        for a list parameter raises a validation error.
        """
        data = {
            "name": "fake_names",
            "parameter_type": "list",
            "provider": "first_name_nonbinary",
        }
        with self.assertRaises(ValidationError):
            FakeBodyParameter(**data)

    def test_max_list_elements(self):
        """
        Test that creating a FakeBodyParameter with a list
        of a length greater than 900 raise a ValidationError.
        """
        data = {
            "name": "fake_names",
            "parameter_type": "list",
            "count": 1000,
            "items": {"parameter_type": "str"},
            "provider": "first_name_nonbinary",
        }
        with self.assertRaises(ValidationError):
            FakeBodyParameter(**data)


if __name__ == "__main__":
    unittest.main()
