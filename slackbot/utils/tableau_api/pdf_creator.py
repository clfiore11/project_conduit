# Import libraries
import os
import typing as T
from pathlib import Path
from dotenv import load_dotenv
from urllib import parse
from tableau_api_lib import TableauServerConnection
from tableau_api_lib.utils import flatten_dict_column
from tableau_api_lib.utils.querying import get_views_dataframe

# Define the environment path
env_path = Path(".") / '.env'
load_dotenv()


def generate_pdf(name, tab, filterable : T.Union[str, None], filters: T.Union[str, None]):
    """
    generate_pdf produces a pdf file from a tableau dashboard.

        name: provide the name of the dashbooard.
        tab: provide the tab of the dashboard.
        filterable: provide the filter your would like to apply.
        filters: provide a item(s) you would like to filter by.

    return: after the process has concluded, it will return a message confirming the pdf has been generated.
    """ 

    # Login to the Tableau Instance
    tableau_server_config = {
            os.environ['environment']: {
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
        print('none')
        # Downloading the default view as it appears on the dashboard
        pdf_params = {
            'type': 'type=unspecified',
            'orientation': 'orientation=Landscape',}

        # Query PDF from Tableau Server
        pdf_view = conn.query_view_pdf(view_id=vid,parameter_dict=pdf_params)   

        # Save File to specified path 

        os.chdir('../googledrive_api/files')
        with open('default.pdf', 'wb') as pdf_file:
            pdf_file.write(pdf_view.content)
        
    else:
        name_list = list(filters)

        #TODO: Ensure list of strings and individual string work on this. 
        name_filter_field = parse.quote(filterable)
        
        for i in name_list:
            # name_filter_value = parse.quote(i)
            name_filter_value = i

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
            os.chdir('../googledrive_api/files')
            with open(pdf_title_string, 'wb') as pdf_file:
                pdf_file.write(pdf_view.content)
            

    # Log out
    conn.sign_out()
    return "Process complete. The PDF has been generated."


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('name', help="Dashboard Name")
    parser.add_argument('tab', help="Dashboard Tab")
    parser.add_argument('filter', help="Dashboard Filter")
    parser.add_argument('value', help="Value(s)")
    args = parser.parse_args()

    try:
        v = None if args.value == 'None' else args.value
        generate_pdf(args.name, args.tab, args.filter, v)

    except Exception as e:
        print(e)