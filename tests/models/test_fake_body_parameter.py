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
                FakeBodyParameter(**data).generate_value(),
                int,
            )
        except Exception as e:
            self.fail(f"Unexpected exception raised: {e}")

    def test_valid_primitive_body_parameter_with_provider(self):
        """
        Test that creating a FakeBodyParameter with a valid primitive 'value'
        does not raise any exceptions.
        """
        try:
            data = {"name": "fake_date", "type": "str", "provider": "date"}
            self.assertRegex(
                FakeBodyParameter(**data).generate_value(),
                r"^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$",
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
            "type": "list",
            "provider": "first_name_nonbinary",
        }
        with self.assertRaises(ValidationError):
            FakeBodyParameter(**data)

    def test_valid_list_value_parameter(self):
        """
        Test that creating a FakeBodyParameter with a valid list 'value'
        does not raise any exceptions.
        """
        try:
            data = {
                "name": "fake_names",
                "type": "list",
                "items": {"type": "str"},
                "provider": "first_name_nonbinary",
            }
            self.assertEqual(
                len(FakeBodyParameter(**data).generate_value()),
                10,
            )
        except Exception as e:
            self.fail(f"Unexpected exception raised: {e}")

    def test_nested_list(self):
        """
        Test that creating a FakeBodyParameter with nested lists
        does not raise any exceptions.
        """
        try:
            data = {
                "name": "fake_names",
                "type": "list",
                "items": {"type": "list", "items": {"type": "str"}},
                "provider": "first_name_nonbinary",
            }
            body_parameters = FakeBodyParameter(**data).generate_value()

            self.assertEqual(
                len(body_parameters),
                10,
            )
            self.assertEqual(
                len(body_parameters[0]),
                10,
            )
            self.assertIsInstance(
                body_parameters[0][0],
                str,
            )
        except Exception as e:
            self.fail(f"Unexpected exception raised: {e}")

    def test_max_list_elements(self):
        """
        Test that creating a FakeBodyParameter with a list
        of a length greater than 900 raise a ValidationError.
        """
        data = {
            "name": "fake_names",
            "type": "list",
            "count": 1000,
            "items": {"type": "str"},
            "provider": "first_name_nonbinary",
        }
        with self.assertRaises(ValidationError):
            FakeBodyParameter(**data).generate_value()


if __name__ == "__main__":
    unittest.main()
