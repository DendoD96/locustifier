import unittest


class TestSample(unittest.TestCase):
    def test_ok(self):
        """
        Simple test case
        """
        self.assertEqual(2 + 3, 5)


if __name__ == "__main__":
    unittest.main()
