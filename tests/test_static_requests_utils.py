import unittest

from static.requests.utils import generate_value


class TestStaticRequestUtils(unittest.TestCase):
    # Necessary to print multiline test description.
    def shortDescription(self):
        return None

    def test_valid_primitive_body_parameter_with_provider(self):
        """
        Test that creating a FakeBodyParameter with a valid primitive 'value'
        does not raise any exceptions.
        """
        try:
            self.assertRegex(
                generate_value(parameter_type="str", provider="date"),
                r"^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$",
            )
        except Exception as e:
            self.fail(f"Unexpected exception raised: {e}")

    def test_valid_list_value_parameter(self):
        """
        Test that creating a FakeBodyParameter with a valid list 'value'
        does not raise any exceptions.
        """
        try:
            self.assertEqual(
                len(
                    generate_value(
                        provider="first_name_nonbinary",
                        parameter_type="list",
                        count=10,
                        items={"type": "str"},
                    )
                ),
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
            body_parameters = generate_value(
                parameter_type="list",
                count=10,
                provider="first_name_nonbinary",
                items={"type": "list", "items": {"type": "str"}},
            )

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


if __name__ == "__main__":
    unittest.main()
