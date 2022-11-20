import typing as T
from slack_bolt import App
import re


class FileUploadButton:
    def __init__(
        self, app: App, name: str, channels: T.Union[T.List, str], file_path: str
    ):
        self.app = app
        self.name = name
        self.channels = channels
        self.file_path = file_path
        self.action_id = f"{self.name}_button_clicked"

    def __dict__(self):
        return (
            {
                "type": "button",
                "text": {"type": "plain_text", "text": f"{self.name}"},
                "action_id": f"{self.action_id}",
            },
        )

    def upload_file(self, channel):
        self.app.client.files_upload_v2(channels=channel, file=self.file_path)
