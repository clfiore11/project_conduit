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



### Tableau API Instructions