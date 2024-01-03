from http import HTTPMethod
import unittest

from pydantic import ValidationError
from sample.models.fake_body_parameter import FakeBodyParameter

from sample.models.locust_task import LocustTask


class TestLocustTask(unittest.TestCase):
    # Necessary to print multiline test description.
    def shortDescription(self):
        return None

    def test_request_body_not_allowed(self):
        """
        Test that creating a LocustTask with a request body incompatible with
        the http method (method different from POST, PUT, PATCH)
        raises a ValidationError.
        """
        with self.assertRaises(ValidationError):
            LocustTask(
                name="fake",
                method=HTTPMethod.GET,
                path="/fake",
                req_body=[FakeBodyParameter(name="fake_argument", type="int")],
            )
