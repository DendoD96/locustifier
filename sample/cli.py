from typing import Optional

from pydantic import ValidationError
import typer

from sample import __app_name__, __version__
from sample.controllers.code_generator import CodeGenerator

app = typer.Typer()


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.command()
def generate(
    spec_file: str = typer.Option(
        None, "--spec-file", "-spec", prompt="specification file location?"
    )
) -> None:
    try:
        CodeGenerator(spec_file).generate()
        typer.secho(
            "Locust code generated correctly :)",
            fg=typer.colors.GREEN,
        )
        raise typer.Exit(0)
    except ValidationError as error:
        typer.secho(
            f"An error occurred during code generation. \
                Details: {error.json()}",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    except FileNotFoundError:
        typer.secho(
            "Specification file not found.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    except ValueError:
        typer.secho(
            "Unsupported file format. Only yaml and json file are supported.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return
