# Project Conduit

More and more workflows are being integrated into messaging suites (like Slack) to empower teams when and where they're collaborating. Access to data and insights shouldn't be any different. This project was started to empower data teams with an open-source toolkit they can use to streamline access and sharing of data and insights.

## Default Tech Stack
The initial project is setup to integrate the following applications:
### Slack
 `/slackbot` directory includes code needed to initialize a slack bot that can be installed in your workspace with the following features:
 - Fetch Tableau PDF

### Google Drive
`/googledrive_api` directory includes scripts that enable you to upload local files to a specficied folder in your google drive. These scripts can be ran independently, or can be used by your slack bot to store dashboard snapshots when fetching dashboard from Tableau.

### Tableau
`/pdf` directory contains scripts that enable you to access Tableau via API and pull .pdf files of existing views in your workspace. These scripts can be ran independently or can be used by your slack bot to fetch dashboard views upon user request.


## Initial Installation Instructions
### Base Project Environment
1. Clone or fork this repo.
2. Setup local environment by running: `python3 -m venv .venv --prompt "project_conduit"`
3. Install modules by running `pip install -r requirements.txt`

### Google Drive API Instructions
1. Follow instructions below from [Quickstart Authentication](https://pythonhosted.org/PyDrive/quickstart.html#authentication):

    > 1. Go to APIs Console and make your own project.
    > 2. Search for ‘Google Drive API’, select the entry, and click ‘Enable’.
    > 3. Select ‘Credentials’ from the left menu, click ‘Create Credentials’, select ‘OAuth client ID’.
    > 4. Now, the product name and consent screen need to be set -> click ‘Configure consent screen’ and
    > allow the instructions. Once finished:
    >   - Select ‘Application type’ to be Web application.
    >   - Enter an appropriate name.
    >   - Input http://localhost:8080 for ‘Authorized JavaScript origins’.
    >   - Input http://localhost:8080/ for ‘Authorized redirect URIs’.
    > 5. Click ‘Save’.
    > 6. Click `Download JSON` on the right side of Client ID to download client_secret_<really long ID>.   json.
    > The downloaded file has all authentication information of your application. **Rename the file to  “client_secrets.json” and place it in your working directory.**

2. Create `googledrive_api/settings.yaml` by following this sample [file](https://pythonhosted.org/PyDrive/oauth.html#sample-settings-yaml)


### Tableau API Instructions
* Follow instructions below from [tableau-api-lib overview](https://pypi.org/project/tableau-api-lib/):

Create a `.env` file and copy the code below to hold your environment variables and secrets. 

```
server=https://<hostname>/
api_version=3.12
personal_access_token_name= <access_token_name>
personal_access_token_secret=<token_secret>
site_name=<site_name>
site_url=<site_url>
environment=<enviornment_name>
```

API Version:  
* To find [API Versions](https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_concepts_versions.html/), use this resource provided by Tableau.


Generating Token Name and Secrets:  
* Login to Tableau and navigate to the 'My Account Settings' page.
* Navigate to the 'Personal Access Tokens' section and input a `token name` of your choice. This will generate an associated token name and `secret key` that we will use in the code above. 


Site Name and URL:
* `site_url`, also known as the content URL, and `site_name` is a segment of the URL that indicates the site you are logging into. You can verify what your site_url and site name is by navigating to your site in your browser, and identifying how your site appears in the URL path.

[Optional] Enviornment:
*  If you have multiple Tabeleau Server instances, use environment to delineate between them. This information is typically held by your Tableau admin. 

