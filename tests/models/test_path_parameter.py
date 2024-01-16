import unittest

from pydantic import ValidationError

from sample.models.path_parameter import PathParameter


class TestPathParameter(unittest.TestCase):
    # Necessary to print multiline test description.
    def shortDescription(self):
        return None

    def test_invalid_style(self):
        """
        Test that creating a PathParameter with an invalid 'style'
        property raises a ValidationError.
        """
        data = {"name": "fake_argument", "value": 1, "style": "fake"}

        with self.assertRaises(ValidationError):
            PathParameter(**data)


if __name__ == "__main__":
    unittest.main()
