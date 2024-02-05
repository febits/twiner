import requests

from twiner.config import TwinerConfig


class Streamer:
    "Define a way to agroup Twitch streamers info."

    def __init__(
        self,
        username,
        usericon,
        stream_title="",
        is_streaming=False,
        previously_shown=False,
    ):
        self.username = username
        self.usericon = usericon
        self.stream_title = stream_title
        self.is_streaming = is_streaming
        self.previously_shown = previously_shown


class Twitch:
    "Defines a structure to store information and actions from Twitch."

    def __init__(self, config: TwinerConfig):
        self.users = [
            Streamer(user, icon)
            for user, icon in config.yaml["tonotify"].items()
        ]
        self.api_oauth_token = "https://id.twitch.tv/oauth2/token"

    def get_access_token(self, client_id, client_secret):
        r = requests.post(
            self.api_oauth_token,
            data={
                "client_id": client_id,
                "client_secret": client_secret,
                "grant_type": "client_credentials",
            },
        )

        return r

    def is_user_streaming(self): ...

    def is_user_valid(self): ...

    def download_usericon(self): ...

    def notification_loop(self): ...
