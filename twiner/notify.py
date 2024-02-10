from plyer import notification

from twiner.config import TwinerConfig
from twiner.twitch import Streamer


def send_notify(user: Streamer, config: TwinerConfig):
    notification.notify(
        title=user.username,
        message=user.stream_title,
        app_name="Twiner",
        timeout=config.yaml["geral"]["notification_timeout"],
        app_icon=(
            user.usericon if config.yaml["geral"]["show_user_picture"] else ""
        ),
    )
