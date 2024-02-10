from os import getenv
from random import randint
from sys import maxsize as MAXINT

from dotenv import load_dotenv
from pytest import mark
from typer.testing import CliRunner

from twiner import __appname__, __version__
from twiner.cli import add, app, configure, init, list, refresh, remove, start
from twiner.config import TwinerConfig
from twiner.twitch import Twitch

runner = CliRunner()
DEFAULT_TEST_CONFIG_PATH = f"/tmp/twiner-{randint(1, MAXINT)}/twiner.yaml"

twitch_users = [
    "cellbit",
    "felps",
    "thegameawards",
    "theprimeagen",
    "calango",
    "leocharada",
    "tsoding",
    "pcinii",
    "rickfernello",
    "bakagaijinlive",
    "doutorbiscoito",
    "g0ularte",
    "quackity",
    "bagi",
    "manodeyvin",
    "lowlevellearning",
]

load_dotenv()


def test_help_flag():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert add.__name__ in result.stdout
    assert remove.__name__ in result.stdout
    assert configure.__name__ in result.stdout
    assert start.__name__ in result.stdout
    assert refresh.__name__ in result.stdout
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


@mark.parametrize(
    "flag,expected",
    [("--config", DEFAULT_TEST_CONFIG_PATH), ("-c", DEFAULT_TEST_CONFIG_PATH)],
)
def test_list_subcommand_fail_case(flag, expected):
    result = runner.invoke(
        app, ["list", flag, DEFAULT_TEST_CONFIG_PATH + str(randint(1, MAXINT))]
    )
    assert result.exit_code == 1
    assert expected not in result.stdout


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


@mark.parametrize(
    "flag,expected",
    [("--config", DEFAULT_TEST_CONFIG_PATH), ("-c", DEFAULT_TEST_CONFIG_PATH)],
)
def test_configure_subcommand_fail_case(flag, expected):
    result = runner.invoke(
        app,
        ["configure", flag, DEFAULT_TEST_CONFIG_PATH],
        input=f"a\na\n",
    )

    assert result.exit_code == 1
    assert expected not in result.stdout


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
def test_add_subcommand(flag, expected):
    config = TwinerConfig(DEFAULT_TEST_CONFIG_PATH)
    config.read_from_config()

    twitch = Twitch(config)

    for user in twitch_users:
        if twitch.is_user_valid(user):
            result = runner.invoke(
                app, ["add", user, flag, DEFAULT_TEST_CONFIG_PATH]
            )

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
def test_add_subcommand_fail_case(flag, expected):
    result = runner.invoke(
        app, ["add", str(randint(1, MAXINT)), flag, DEFAULT_TEST_CONFIG_PATH]
    )

    assert result.exit_code == 1
    assert expected not in result.stdout


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
def test_refresh_subcommand(flag, expected):
    result = runner.invoke(app, ["refresh", flag, DEFAULT_TEST_CONFIG_PATH])

    assert result.exit_code == 0
    assert expected in result.stdout


@mark.parametrize(
    "flag,expected",
    [("--config", DEFAULT_TEST_CONFIG_PATH), ("-c", DEFAULT_TEST_CONFIG_PATH)],
)
def test_refresh_subcommand_fail_case(flag, expected):
    result = runner.invoke(
        app,
        ["refresh", flag, DEFAULT_TEST_CONFIG_PATH + str(randint(1, MAXINT))],
    )

    assert result.exit_code == 1
    assert expected not in result.stdout


@mark.skipif(
    not getenv("CLIENTID") and not getenv("CLIENTSECRET"),
    reason="You have to set CLIENTID and CLIENTSECRET env vars. Create a "
    ".env file or pass through the pytest call. For example: CLIENTID=X "
    "CLIENTSECRET=Y make test",
)
@mark.parametrize(
    "flag,expected",
    [("--config", DEFAULT_TEST_CONFIG_PATH)],
)
def test_delete_subcommand(flag, expected):
    for user in twitch_users:
        result = runner.invoke(
            app, ["remove", user, flag, DEFAULT_TEST_CONFIG_PATH]
        )

        assert result.exit_code == 0
        assert expected in result.stdout


@mark.parametrize(
    "flag,expected",
    [("--config", DEFAULT_TEST_CONFIG_PATH)],
)
def test_delete_subcommand_fail_case(flag, expected):
    result = runner.invoke(
        app,
        ["remove", str(randint(1, MAXINT)), flag, DEFAULT_TEST_CONFIG_PATH],
    )

    assert result.exit_code == 1
    assert expected not in result.stdout


def change_credentials():
    config = TwinerConfig(DEFAULT_TEST_CONFIG_PATH)
    config.read_from_config()

    config.yaml["creds"]["access_token"] = str(randint(1, MAXINT))
    config.yaml["creds"]["client_id"] = str(randint(1, MAXINT))
    config.write_to_config(config.yaml)


@mark.parametrize(
    "flag,expected",
    [("--config", "Invalid credentials"), ("-c", "Invalid credentials")],
)
def test_add_subcommand_fail_case_invalid_credentials(flag, expected):
    change_credentials()
    result = runner.invoke(
        app,
        ["add", str(randint(1, MAXINT)), flag, DEFAULT_TEST_CONFIG_PATH],
    )

    assert result.exit_code == 1
    assert expected in result.stdout


@mark.parametrize(
    "flag,expected",
    [("--config", "Invalid credentials"), ("-c", "Invalid credentials")],
)
def test_refresh_subcommand_fail_case_invalid_credentials(flag, expected):
    change_credentials()
    result = runner.invoke(
        app,
        ["refresh", flag, DEFAULT_TEST_CONFIG_PATH],
    )

    assert result.exit_code == 1
    assert expected in result.stdout


@mark.parametrize(
    "flag,expected",
    [("--config", "Invalid credentials"), ("-c", "Invalid credentials")],
)
def test_start_subcommand_fail_case_invalid_credentials(flag, expected):
    change_credentials()
    result = runner.invoke(
        app,
        ["start", flag, DEFAULT_TEST_CONFIG_PATH],
    )

    assert result.exit_code == 1
    assert expected in result.stdout
