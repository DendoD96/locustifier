import unittest
from typer.testing import CliRunner

from locustifier import __app_name__, __version__, cli


class TestCli(unittest.TestCase):

    def __init__(self, methodName) -> None:
        super().__init__(methodName)
        self.runner = CliRunner()

    # Necessary to print multiline test description.
    def shortDescription(self):
        return None

    def test_version(self):
        result = self.runner.invoke(cli.app, ["--version"])
        assert result.exit_code == 0
        assert f"{__app_name__} v{__version__}\n" in result.stdout
