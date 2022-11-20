import logging
import os
import re

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.errors import SlackApiError
from messages.greeting import GREETING
from messages.mention import MENTION_REPLY
from buttons.file_upload_button import FileUploadButton

# load env variables from .env file
load_dotenv()

SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
SLACK_BOT_TOKEN = os.environ["SLACKBOT_TOKEN"]

app = App(token=SLACK_BOT_TOKEN, name="Project Conduit")
logger = logging.getLogger(__name__)


# define buttons
meal_prep_button = FileUploadButton(
    app=app,
    name="Fetch Meal Prep",
    channels="C04CE7NKNG0",
    file_path="/Users/cfiore/Documents/GitHub/project_conduit/googledrive_api/files/test.png",
)


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
            # buttons
            {"type": "actions", "elements": [meal_prep_button.__dict__()[0]]},
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
                    "text": f"{MENTION_REPLY}",
                },
            },
        ],
    )


@app.action(meal_prep_button.action_id)
def button_click_action(body, ack, say):
    ack(),
    say({"text": "Grabbing that tasty meal!"})
    meal_prep_button.upload_file(channel=body["user"]["id"])


def main():
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()


# start app
if __name__ == "__main__":
    main()
