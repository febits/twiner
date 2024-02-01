from typing import Optional

import typer
from rich.console import Console
from typing_extensions import Annotated

from twiner import __appname__, __version__

app = typer.Typer(help="🎮 Twiner CLI (Twitch Notifier)")
console = Console()


def version(value: bool):
    """Callback that shows the current version."""
    if value:
        console.print(__appname__, __version__)
        raise typer.Exit(0)


@app.callback()
def main(
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version",
            "-v",
            "-V",
            help="Show the current version.",
            is_flag=True,
            callback=version,
        ),
    ] = False
): ...
