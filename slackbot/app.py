import logging
import os
import re

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.errors import SlackApiError
from messages.greeting import GREETING

# load env variables from .env file
load_dotenv()

SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
SLACK_BOT_TOKEN = os.environ["SLACKBOT_TOKEN"]

app = App(token=SLACK_BOT_TOKEN, name="Project Conduit")
logger = logging.getLogger(__name__)


@app.message("hello")
def message_hello(message, say):
    say(
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Hello <@{message['user']}>! Here's what's new:\n{GREETING}",
                },
            },
        ],
    )


@app.event("app_mention")
def mention_reply(body, say):
    say(
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"KEEP MY WIFES NAME OUT YA MOUTH",
                },
            },
        ],
    )


def main():
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()


# start app
if __name__ == "__main__":
    main()
