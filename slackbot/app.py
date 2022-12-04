# Import libraries
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

# Load env variables from .env file
load_dotenv()

# Slack App and Bot Tokens
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]

# Assigning app correct token
app = App(token=SLACK_BOT_TOKEN)
logger = logging.getLogger(__name__)

# Configure buttons with specific actions
pdf1 = FileUploadButton(
    app=app,
    name="Report: Manager 1",
    channels="xoxp-439",
    manager='Jane Doe',
    file_path="files/Jane_Doe.pdf",
)

pdf2 = FileUploadButton(
    app=app,
    name="Report: Manager 2",
    channels="xoxp-439",
    manager = 'John Wayne',
    file_path="files/John_Wayne.pdf",
)

pdf3 = FileUploadButton(
    app=app,
    name="Report: Manager 3",
    channels="xoxp-439",
    manager = 'Syliva Matthews',
    file_path="files/Syliva_Matthews.pdf",
)

pdf4 = FileUploadButton(
    app=app,
    name="Report: Manager 4",
    channels="xoxp-439",
    manager='Varshi Ike',
    file_path="files/Varshi_Ike.pdf",
)

# Slack Socket to Listen for the world hello
list_of_words = ['hello', 'Hello', 'Hi','hi','report', 'Report']
words_re = re.compile("|".join(list_of_words))

@app.message(words_re)
def message_hello(message, say):
    """
    message_hello does x, y, z

        message: 
        say: 

    return: no explicit return statement or value.

    """

    say(
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Hello <@{message['user']}>. {GREETING}",
                },
            },
            # Buttons for user to see
            {"type": "actions", "elements": [pdf1.__dict__()[0]]},
            {"type": "actions", "elements": [pdf2.__dict__()[0]]},
            {"type": "actions", "elements": [pdf3.__dict__()[0]]},
            {"type": "actions", "elements": [pdf4.__dict__()[0]]},
        ],
    )


@app.event("app_mention")
def mention_reply(body, say):
    """
    message_hello does x, y, z

        body: 
        say: 

    return: no explicit return statement or value.

    """

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


# Configure actions for each button
@app.action(pdf1.action_id)
def button_click_action(body, ack, say):
    ack(),
    say({"text": "Grabbing your requested PDF!"})
    pdf1.upload_file(body["user"]["id"],pdf1.manager)


@app.action(pdf2.action_id)
def button_click_action(body, ack, say):
    ack(),
    say({"text": "Grabbing your requested PDF!"})
    pdf2.upload_file(body["user"]["id"],pdf2.manager)    

@app.action(pdf3.action_id)
def button_click_action(body, ack, say):
    ack(),
    say({"text": "Grabbing your requested PDF!"})
    pdf3.upload_file(body["user"]["id"],pdf3.manager)


@app.action(pdf4.action_id)
def button_click_action(body, ack, say):
    ack(),
    say({"text": "Grabbing your requested PDF!"})
    pdf4.upload_file(body["user"]["id"],pdf4.manager)  


def main():
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()


# start app
if __name__ == "__main__":
    main()