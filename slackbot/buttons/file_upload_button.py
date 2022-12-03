import typing as T
from slack_bolt import App
import os

from utils.googledrive_api.gdrive_update_upload import gdrive_update_upload
from utils.tableau_api.pdf_creator import generate_pdf

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

        owd = os.getcwd()

        # change dir to function dir
        os.chdir("utils/tableau_api")
        
        # generate pdf
        #TODO: Remember to change these args
        generate_pdf('[Draft] NPS One Pagers Mock up', 'NPSOnePagerDIRECTROLLUP', 'Manager', None)
       
        # change dir to function dir
        os.chdir("../")
        
        # upload fresh file to gdrive
        gdrive_update_upload(folder_id="1X3Qew8QlzOWwhtFjYOBtfMqaVnvEzRye")

        self.app.client.files_upload(channels=channel, file=self.file_path)

        os.chdir(owd)
