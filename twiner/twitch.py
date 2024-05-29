import time
from datetime import datetime
from typing import Callable

import requests
import wget
from rich.console import Console

from twiner.config import TwinerConfig

console = Console()


class Streamer:
    "Define a way to agroup Twitch streamers info."

    def __init__(
        self,
        username: str,
        usericon: str,
        stream_title: str = "",
        viewer_count: int = 0,
        is_streaming: bool = False,
        previously_shown: bool = False,
    ):
        self.username = username
        self.usericon = usericon
        self.stream_title = stream_title
        self.is_streaming = is_streaming
        self.previously_shown = previously_shown
        self.viewer_count = viewer_count


class Twitch:
    "Defines a structure to store information and actions from Twitch."

    def __init__(self, config: TwinerConfig):
        self.users = [
            Streamer(user, icon)
            for user, icon in config.yaml["tonotify"].items()
        ]
        self.api_headers = {
            "Client-Id": f"{config.yaml['creds']['client_id']}",
            "Authorization": f"Bearer {config.yaml['creds']['access_token']}",
        }
        self.api_oauth_token = "https://id.twitch.tv/oauth2/token"
        self.api_users = "https://api.twitch.tv/helix/users"
        self.api_streams = "https://api.twitch.tv/helix/streams"

    def is_api_working(self):
        """Test if the Twitch API is working."""

        try:
            return (
                requests.get(
                    self.api_streams, headers=self.api_headers, timeout=20
                ).status_code
                == 200
            )
        except requests.exceptions.Timeout as e:
            raise requests.exceptions.Timeout("Request has timed out.") from e

    def get_access_token(self, client_id: str, client_secret: str):
        """Obtain Twitch access token."""

        try:
            r = requests.post(
                self.api_oauth_token,
                data={
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "grant_type": "client_credentials",
                },
                timeout=20,
            )

            return r
        except requests.exceptions.Timeout as e:
            raise requests.exceptions.Timeout("Request has timed out.") from e

    def is_user_streaming(self, user: str):
        """Verify if the user is streaming."""

        try:
            r = requests.get(
                self.api_streams + f"?user_login={user}",
                headers=self.api_headers,
                timeout=20,
            )

            if r.status_code == 200:
                if not r.json()["data"]:
                    return False

                return True

            return False
        except requests.exceptions.Timeout as e:
            raise requests.exceptions.Timeout("Request has timed out.") from e

    def is_user_valid(self, user: str):
        """Verify if given user is valid on Twitch."""

        try:
            r = requests.get(
                self.api_users + f"?login={user}",
                headers=self.api_headers,
                timeout=20,
            )
            if r.status_code == 200:
                if not r.json()["data"]:
                    return False

                return True

            return False
        except requests.exceptions.Timeout as e:
            raise requests.exceptions.Timeout("Request has timed out.") from e

    def get_usericon(self, config: TwinerConfig, user: str):
        """Get usericon from a user on Twitch."""

        try:
            r = requests.get(
                self.api_users + f"?login={user}",
                headers=self.api_headers,
                timeout=20,
            )
            if r.status_code == 200:
                icon_url = r.json()["data"][0]["profile_image_url"]
                if not icon_url:
                    return ""

                config.create_datadir()
                output = str(config.datadir / f"{user}.png")
                wget.download(icon_url, out=output)

                return output

            return ""
        except requests.exceptions.Timeout as e:
            raise requests.exceptions.Timeout("Request has timed out.") from e

    def get_streams_info(self, user: str):
        """Get streams info from a Twitch user."""

        try:
            r = requests.get(
                self.api_streams + f"?user_login={user}",
                headers=self.api_headers,
                timeout=20,
            )

            if r.status_code == 200:
                return r.json()["data"][0]

            return {}
        except requests.exceptions.Timeout as e:
            raise requests.exceptions.Timeout("Request has timed out.") from e

    def notification_loop(
        self,
        config: TwinerConfig,
        notify: Callable[[Streamer, TwinerConfig], None],
    ):
        "The notification loop of twitch users from config."

        counter = 1
        while True:
            console.print(
                f"< Loop {counter} : {datetime.now().strftime('%H:%M:%S')} >"
            )
            for user in self.users:
                if self.is_user_streaming(user.username):
                    if user.previously_shown:
                        continue

                    user.is_streaming = True
                    user.previously_shown = True

                    stream_title = self.get_streams_info(user.username)[
                        "title"
                    ]
                    user.stream_title = (
                        stream_title
                        if len(stream_title) < 50
                        else stream_title[:50] + "..."
                    )
                    user.viewer_count = self.get_streams_info(user.username)[
                        "viewer_count"
                    ]

                    console.print(
                        f'\t[b]{user.username}[/]: "{user.stream_title}" - {user.viewer_count} viewers'
                    )
                    console.print(
                        f"\t(ready to notify: [b][i]{user.username}[/])\n"
                    )

                    notify(user, config)
                else:
                    if user.is_streaming:
                        user.is_streaming = False
                        user.previously_shown = False
                        user.stream_title = ""
                        user.viewer_count = 0

            time.sleep(config.yaml["geral"]["loop_period"])
            counter += 1
