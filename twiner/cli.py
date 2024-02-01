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


@app.command()
def add(
    user: Annotated[str, typer.Argument(..., help="Username from Twitch.")]
):
    """Add a user to the notification pool."""
    ...


@app.command()
def remove(
    user: Annotated[str, typer.Argument(..., help="Username from Twitch.")]
):
    """Remove a user from the notification pool."""
    ...


@app.command()
def configure(
    client_id: Annotated[
        str, typer.Option(..., help="Twitch Client ID.", prompt="ℹ️  Client ID")
    ],
    client_secret: Annotated[
        str,
        typer.Option(
            ..., help="Twitch Client Secret.", prompt="🔑 Client Secret"
        ),
    ],
):
    """Configure the Twitch Credentials."""
    ...


@app.command()
def start():
    """Start the notification loop."""
    ...


@app.command()
def list():
    """List the config file fields."""
    ...


@app.command()
def init():
    """Init the config file (it will perform a redefining action through
    the config file, using it exclusively for the initial setup)."""
    ...
