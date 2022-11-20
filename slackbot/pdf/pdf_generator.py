# Import libraries
import os
import typing as T
from slack_bolt import App
from pathlib import Path
from dotenv import load_dotenv
from urllib import parse
from tableau_api_lib import TableauServerConnection
from tableau_api_lib.utils import flatten_dict_column
from tableau_api_lib.utils.querying import get_views_dataframe

# Define the environment path
env_path = Path(".") / '.env'
load_dotenv()

class TableauPDF:
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


    def generate_pdf(self, name, tab, filters: T.Union[T.List, str, None]):
        # Login to the Tableau Instance
        tableau_server_config = {
                'dd_people': {
                        'server': os.environ['server'],
                        'api_version': os.environ['api_version'],
                        'personal_access_token_name': os.environ['personal_access_token_name'],
                        'personal_access_token_secret':os.environ['personal_access_token_secret'],
                        'site_name': os.environ['site_name'],
                        'site_url': os.environ['site_url'],
                }   
            }    

        # Sign in
        conn = TableauServerConnection(tableau_server_config, env = os.environ['environment'])
        conn.sign_in() 

        # Get a dataframe of all the views in tableau
        views_df = get_views_dataframe(conn)

        # Flatten Nested Fields
        views_df = flatten_dict_column(views_df,keys=["name","id"],col_name='workbook')

        # Save view id
        vid = views_df[(views_df['workbook_name'] == name) & (views_df['viewUrlName'] == tab)]['id'].values[0]

        if filters is None:

            # Downloading the default view as it appears on the dashboard
            pdf_params = {
                'type': 'type=unspecified',
                'orientation': 'orientation=Landscape',}

            # Query PDF from Tableau Server
            pdf_view = conn.query_view_pdf(view_id=vid,parameter_dict=pdf_params)   

            # Save File to specified path 
            with open('default.pdf', 'wb') as pdf_file:
                pdf_file.write(pdf_view.content)

        else:
            name_list = list(filters)
            #TODO: Change this param based on the dashboard
            # Parameter to filter on. Right now, it is Manager
            name_filter_field = parse.quote("Manager")
            for i in name_list:
                name_filter_value = parse.quote(i)

                # Downloading the default view as it appears on the dashboard
                pdf_params = {
                'type': 'type=unspecified',
                'orientation': 'orientation=Landscape',
                'filter_name': f"vf_{name_filter_field}={name_filter_value}",
                }

                # Query PDF from Tableau Server
                pdf_view = conn.query_view_pdf(view_id=vid,parameter_dict=pdf_params)
                
                # Rename PDF
                pdf_title_string = i.replace(' ','_') + '.pdf'
                
                # Save File to specified path 
                with open(pdf_title_string, 'wb') as pdf_file:
                    pdf_file.write(pdf_view.content)

        # Log out
        conn.sign_out()
        
    def upload_file(self, channel):
        self.app.client.files_upload_v2(channels=channel, file=self.file_path)

# Tableau = TableauPDF()
# Tableau.generate_pdf('[Draft] NPS One Pagers Mock up' , 'NPSOnePagerDIRECTROLLUP', None)