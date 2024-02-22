# Twiner

Twiner (Twitch Notifier) is a CLI tool designed to assist people with notification support for their favorite streamers, prioritizing simplicity and ease of use.

Features:

- Add a user from Twitch to the notification pool.
- Remove a user from the notification pool.
- Twitch credentials stuff made easy.
- Beautiful, pretty and fancy display.

## Installation

It's possible to install `twiner` via PyPI with pip as shown bellow:
```bash
pip install twiner
```

## Usage

Try what is bellow to receive a general view of how twiner works:
```bash
twiner --help
```

```bash
                                                                                                                                                    
 Usage: twiner [OPTIONS] COMMAND [ARGS]...                                                                                                          
                                                                                                                                                    
 🎮 Twiner CLI (Twitch Notifier)                                                                                                                    
                                                                                                                                                    
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --version             -v,-V        Show the current version.                                                                                     │
│ --install-completion               Install completion for the current shell.                                                                     │
│ --show-completion                  Show completion for the current shell, to copy it or customize the installation.                              │
│ --help                             Show this message and exit.                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ add         Add a user to the notification pool.                                                                                                 │
│ configure   Configure the Twitch Credentials.                                                                                                    │
│ init        Init the config file (it will perform a redefining action through the config file, using it exclusively for the initial setup).      │
│ list        List the config file fields.                                                                                                         │
│ refresh     Refresh the user profile pictures.                                                                                                   │
│ remove      Remove a user from the notification pool.                                                                                            │
│ start       Start the notification loop.                                                                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```

## Examples

Let's suppose that you want to add your favorite stream to the notification pool. I'll exemplify that with mine (cellbit).

Firstly, you need to initialize the config file:
```bash
twiner init
```

After that, you need to enter your Twitch credentials for the API:
```bash
twiner configure
```

It will be requested your `CLIENT_ID` and `CLIENT_SECRET` via stdin (user input). How do you get those credentials?

Follow this: https://dev.twitch.tv/docs/authentication/register-app


Now you are able to add a Twitch user
```bash
twiner add cellbit
```

You also can remove that user:
```bash
twiner remove cellbit
```

To start the notification loop, you need to run:
```bash
twiner start
```

Extras:

You can list your entire config running:
```bash
twiner list
```

And you can refresh the user data (profile user image) running:
```bash
twiner refresh
```

The 'twiner refresh' above is supposed to update the profile images of your streamers added (if they updated them)
