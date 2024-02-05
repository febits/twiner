from os import getenv
from random import randint
from sys import maxsize as MAXINT

from dotenv import load_dotenv
from pytest import mark
from typer.testing import CliRunner

from twiner import __appname__, __version__
from twiner.cli import add, app, configure, init, list, remove, start

runner = CliRunner()
DEFAULT_TEST_CONFIG_PATH = f"/tmp/twiner-{randint(1, MAXINT)}/twiner.yaml"

load_dotenv()


def test_help_flag():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert add.__name__ in result.stdout
    assert remove.__name__ in result.stdout
    assert configure.__name__ in result.stdout
    assert start.__name__ in result.stdout
    assert init.__name__ in result.stdout
    assert list.__name__ in result.stdout


@mark.parametrize(
    "flag,expected",
    [
        ("--version", f"{__appname__} {__version__}"),
        ("-v", f"{__appname__} {__version__}"),
        ("-V", f"{__appname__} {__version__}"),
    ],
)
def test_version_flag(flag, expected):
    result = runner.invoke(app, [flag])
    assert result.exit_code == 0
    assert expected in result.stdout


@mark.parametrize(
    "flag,expected",
    [("--config", DEFAULT_TEST_CONFIG_PATH), ("-c", DEFAULT_TEST_CONFIG_PATH)],
)
def test_init_subcommand(flag, expected):
    result = runner.invoke(app, ["init", flag, DEFAULT_TEST_CONFIG_PATH])
    assert result.exit_code == 0
    assert expected in result.stdout


@mark.parametrize(
    "flag,expected",
    [("--config", DEFAULT_TEST_CONFIG_PATH), ("-c", DEFAULT_TEST_CONFIG_PATH)],
)
def test_list_subcommand(flag, expected):
    result = runner.invoke(app, ["list", flag, DEFAULT_TEST_CONFIG_PATH])
    assert result.exit_code == 0
    assert expected in result.stdout


@mark.skipif(
    not getenv("CLIENTID") and not getenv("CLIENTSECRET"),
    reason="You have to set CLIENTID and CLIENTSECRET env vars. Create a "
    ".env file or pass through the pytest call. For example: CLIENTID=X "
    "CLIENTSECRET=Y make test",
)
@mark.parametrize(
    "flag,expected",
    [("--config", DEFAULT_TEST_CONFIG_PATH), ("-c", DEFAULT_TEST_CONFIG_PATH)],
)
def test_configure_subcommand(flag, expected):
    result = runner.invoke(
        app,
        ["configure", flag, DEFAULT_TEST_CONFIG_PATH],
        input=f"{getenv('CLIENTID')}\n{getenv('CLIENTSECRET')}\n",
    )

    assert result.exit_code == 0
    assert expected in result.stdout
