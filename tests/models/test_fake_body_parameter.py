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
        data = {"name": "fake_argument", "type": "mycustomfaketype"}

        with self.assertRaises(ValidationError):
            FakeBodyParameter(**data)

    def test_valid_primitive_body_parameter(self):
        """
        Test that creating a FakeBodyParameter with a valid primitive 'value'
        does not raise any exceptions.
        """
        try:
            data = {"name": "fake_argument", "type": "int"}
            self.assertIsInstance(
                FakeBodyParameter(**data),
                FakeBodyParameter,
            )
        except Exception as e:
            self.fail(f"Unexpected exception raised: {e}")


if __name__ == "__main__":
    unittest.main()
