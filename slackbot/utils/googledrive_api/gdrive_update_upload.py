import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import logging

if not os.path.exists("debug_logs"):
    os.makedirs("debug_logs")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug_logs/gdrive_update_upload_debug.log"),
        logging.StreamHandler(),
    ],
)


def gdrive_update_upload(folder_id: str):
    """
    gdrive_update_upload will scan the google drive and upload values as things are 

        folder_id: The folder_id is the destination location for the item we would like to upload

    return: no explicit return statement or value.

    """


    try:
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        drive = GoogleDrive(gauth)
    except Exception as e:
        print(e)

    
    upload_file_dict = {
        os.path.join("files", file).split("/")[-1]: os.path.join("files", file)
        for file in os.listdir("files")
    }

    logging.info(f"Files to be updated/uploaded: {upload_file_dict.keys()}...")
    gfiles = drive.ListFile(
        {"q": f"'{folder_id}' in parents and trashed=false"}
    ).GetList()

    gfile_dict = {file["title"]: file["id"] for file in gfiles}
    for file_name in upload_file_dict:
        try:
            if file_name in gfile_dict:
                logging.info(f"{file_name} file located in google drive...")
                file = drive.CreateFile({"id": f"{gfile_dict[file_name]}"})
                file.SetContentFile(upload_file_dict[file_name])
                logging.info(f"Updating {file_name} file contents...")
                file.Upload()
                logging.info("File successfully updated!")

            if file_name not in gfile_dict.keys():
                logging.info(f"{file_name} file not located in google drive...")
                file = drive.CreateFile(
                    {"parents": [{"id": folder_id}], "title": f"{file_name}"}
                )

                file.SetContentFile(upload_file_dict[file_name])
                logging.info(f"Uploading {file_name} file contents...")
                file.Upload()
                logging.info("File successfully uploaded!")

        except Exception as e:
            print(e)

if __name__ == "__main__":
    import argparse

    # define default args
    default_folder_id = "1X3Qew8QlzOWwhtFjYOBtfMqaVnvEzRye"

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--folder_id",
        help="Target gdrive folder id, found in url.",
        default=default_folder_id,
    )
    args = parser.parse_args()

    try:
        gdrive_update_upload(folder_id=args.folder_id)
    except Exception as e:
        print(e)
