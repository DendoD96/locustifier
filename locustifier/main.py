from . import cli
from . import __app_name__


def main():
    cli.app(prog_name=__app_name__)
