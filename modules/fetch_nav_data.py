# ----------------------------------------------------------------------------------
# Author: Amaresh M
# Email: m[dot]amaresh[at]hotmail[dot]com
# File Name: [fetch_nav_data.py]
# Description: [Brief description of the file's purpose]
# ----------------------------------------------------------------------------------

import os
import requests
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the URL to fetch the data
AMFI_URL = "https://www.amfiindia.com/spages/NAVAll.TXT"

# Define the path for saving the file
TEMP_DATA_DIR = "temp_data"  # Create a directory for storing data files
os.makedirs(TEMP_DATA_DIR, exist_ok=True)


# Function to fetch and process NAVAll.txt
def fetch_nav_data():
    try:
        logger.info("Fetching data from the URL...")
        # Fetch the data from the URL
        response = requests.get(AMFI_URL)
        data = response.text

        logger.info("Generating file name...")
        # Generate a file name based on the current date
        today = datetime.now()
        file_name = f"NAVAll_{today.strftime('%d_%b_%Y')}.txt"
        print(file_name)

        logger.info(f"Saving data to {file_name}...")
        # Save the processed data to the file
        with open(
            os.path.join(TEMP_DATA_DIR, file_name), "w", encoding="utf-8"
        ) as file:
            file.write(data)

        logger.info(f"Data saved to {file_name}")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    fetch_nav_data()
