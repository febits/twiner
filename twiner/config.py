from os import getenv
from pathlib import Path
from typing import Dict

import yaml


class TwinerConfig:
    """Define a way/wrapper for the application to manipulate the config
    aspects."""

    DEFAULT_CONFIG_PATH = f"{getenv('HOME')}/.config/twiner/twiner.yaml"
    DEFAULT_DATA_DIR = f"{getenv('HOME')}/.local/share/twiner"

    def __init__(self, path: str | None):
        self.template = {
            "geral": {
                "loop_period": 300,
                "notification_timeout": 5,
                "show_user_picture": True,
            },
            "creds": {
                "client_id": "",
                "client_secret": "",
                "access_token": "",
                "expires_in": 0,
            },
            "tonotify": {},
        }
        self.yaml = {}
        self.path = Path(path)
        self.datadir = Path(self.DEFAULT_DATA_DIR)

    def write_to_config(self, data: Dict[str, Dict]):
        """Write the given data to the config file."""

        if not self.path.exists():
            self.path.parent.mkdir(mode=0o744, exist_ok=True)
            self.path.touch(mode=0o644)

        yaml.dump(data, self.path.open(mode="w"))

    def read_from_config(self):
        """Read the config file."""

        self.yaml = yaml.safe_load(self.path.open(mode="r"))

    def create_datadir(self):
        """Create data dir where will be stored the usericons."""

        self.datadir.mkdir(mode=0o755, parents=True, exist_ok=True)
