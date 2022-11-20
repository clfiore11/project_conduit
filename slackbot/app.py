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
from pdf.pdf_generator import TableauPDF

# Load env variables from .env file
load_dotenv()

# Slack App and Bot Tokens
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]

# Assigning app correct token
app = App(token=SLACK_BOT_TOKEN)
logger = logging.getLogger(__name__)


# Define buttons
pdf = FileUploadButton(
    app=app,
    name="Fetch Tableau PDF",
    channels="xoxp-439",
    file_path="/Users/sylvesterikpa/Desktop/default.pdf",
)


# Define buttons again | Test
tab = TableauPDF(
    app=app,
    name="Fetch Tableau PDF 2",
    channels="xoxp-439",
    file_path="/Users/sylvesterikpa/Desktop/Project 699/project_conduit/default.pdf",
)

# Slack Socket to Listen for the world hello
@app.message("hello")
def message_hello(message, say):
    say(
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Hello <@{message['user']}>. {GREETING}",
                },
            },
            # Buttons
            {"type": "actions", "elements": [pdf.__dict__()[0]]},
            {"type": "actions", "elements": [tab.__dict__()[0]]}
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


@app.action(pdf.action_id)
def button_click_action(body, ack, say):
    ack(),
    say({"text": "Grabbing your requested PDF!"})
    pdf.upload_file(channel=body["user"]["id"])


@app.action(tab.action_id)
def button_click_action(body, ack, say):
    ack(),
    say({"text": "Grabbing your requested PDF!"})
    tab.generate_pdf('[Draft] NPS One Pagers Mock up' , 'NPSOnePagerDIRECTROLLUP', None) # Example 
    pdf.upload_file(channel=body["user"]["id"])


def main():
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()


# start app
if __name__ == "__main__":
    main()
