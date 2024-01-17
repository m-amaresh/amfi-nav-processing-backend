import os
import dropbox
import logging
from datetime import datetime
from dotenv import load_dotenv

# Initialize the logger
logger = logging.getLogger(__name__)

load_dotenv()

# Configuration variables
ACCESS_TOKEN = os.getenv("DROPBOX_TOKEN")
DROPBOX_PATH = "/amfi-nav-processing-backend/historical-nav/"
TEMP_DATA_DIR = "temp_data"

def upload_nav_data():
    try:
        logger.info("Uploading data to Dropbox")

        # Initialize Dropbox client
        dbx = dropbox.Dropbox(ACCESS_TOKEN)

        # List files and folders in the target Dropbox directory
        files_in_dropbox = []
        for entry in dbx.files_list_folder(DROPBOX_PATH).entries:
            if isinstance(entry, dropbox.files.FileMetadata):
                files_in_dropbox.append(entry.name)

        # Define the file path
        today = datetime.now()
        file_name = f"NAVAll_{today.strftime('%d_%b_%Y')}.txt"
        file_path = os.path.join(TEMP_DATA_DIR, file_name)

        # Check if the file already exists in Dropbox
        if file_name in files_in_dropbox:
            logger.info(f"File '{file_name}' already exists on Dropbox. Skipping upload.")
            return

        # Upload the file to Dropbox
        with open(file_path, "rb") as file:
            dbx.files_upload(file.read(), os.path.join(DROPBOX_PATH, file_name))

        logger.info("Data uploaded to Dropbox")

    except Exception as e:
        logger.error(f"An error occurred while uploading to Dropbox: {str(e)}")

def main():
    # Call the upload_nav_data function
    upload_nav_data()

if __name__ == "__main__":
    main()
