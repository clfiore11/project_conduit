import typing as T
from slack_bolt import App
import os

from utils.googledrive_api.gdrive_update_upload import gdrive_update_upload
from utils.tableau_api.pdf_creator import generate_pdf

class FileUploadButton:
    def __init__(
        self, app: App, name: str, channels: T.Union[T.List, str], manager:T.Union[None, str],  file_path: str
    ):
        self.app = app
        self.name = name
        self.channels = channels
        self.manager = manager
        self.file_path = file_path
        self.action_id = f"{self.name}_button_clicked"

    def __dict__(self):
        """"
        __dict__ provided a slack button framework

        return: a button with the elements determined by the user

        """
        return (
            {
                "type": "button",
                "text": {"type": "plain_text", "text": f"{self.name}"},
                "action_id": f"{self.action_id}",
            },
        )

    def upload_file(self, channel, manager):
        """
        upload_file runs the the gdrive_update_upload and generate_pdf fucntions to genereate and store the reports requested.

        channel: the slack channel / dm that the data should be uploaded to.
        manager: preconfigured value for the report that a user would like to request. For demostration purposes, we used manager.

        return: No explicit return statement or value.

        """
        
        # storing current directory
        owd = os.getcwd()

        # change dir to function dir
        os.chdir("utils/tableau_api")
        
        # user can configure this to be any dasboard or tab in tableau
        generate_pdf('[Draft] NPS One Pagers Mock up', 'NPSOnePagerDIRECTROLLUP', 'Manager', [self.manager])
       
        # change dir to function dir
        os.chdir("../")
        
        # upload fresh file to gdrive
        gdrive_update_upload(folder_id="1X3Qew8QlzOWwhtFjYOBtfMqaVnvEzRye")

        self.app.client.files_upload(channels=channel, file=self.file_path)

        # changing directory to the original state
        os.chdir(owd)
