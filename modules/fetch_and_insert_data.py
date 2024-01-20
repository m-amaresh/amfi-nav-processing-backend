import os
from pymongo import MongoClient
from dotenv import load_dotenv
import time
from datetime import datetime
from config.config import (
    TEMP_DATA_DIR,
    NAV_FILE_NAME_FORMAT,
    FUND_HOUSE_FILE_PATH,
    SCHEME_TYPE_FILE_PATH,
)


def load_list_from_file(filename):
    with open(filename, "r") as file:
        return [line.strip().lower() for line in file]


def fetch_and_insert_data():
    try:
        print("Starting the process")

        print("Connecting to MongoDB Atlas")
        mongo_uri = os.getenv("MONGO_URI")
        db_name = os.getenv("DB_NAME")
        collection_name = os.getenv("COLLECTION_NAME")

        client = MongoClient(mongo_uri)
        db = client[db_name]
        collection = db[collection_name]

        # Generate the NAV file name based on the current date
        today = datetime.now()
        nav_file_name = today.strftime(NAV_FILE_NAME_FORMAT)
        nav_file_path = os.path.join(TEMP_DATA_DIR, nav_file_name)

        print(f"Loading and extracting data from AMFI: {nav_file_name}")
        with open(nav_file_path, "r") as file:
            data = file.read().splitlines()

        current_scheme_type = None
        current_fund_house = None

        record_count = 0
        for line in data:
            if line.startswith("Scheme Code"):
                continue

            line_lower = line.lower()

            if line_lower in fund_houses:
                current_fund_house = line
                continue
            elif line_lower in scheme_types:
                current_scheme_type = line
                continue

            fields = line.split(";")
            if len(fields) == 6:
                record_dict = {
                    "scheme_type": current_scheme_type,
                    "fund_house": current_fund_house,
                    "scheme_code": fields[0],
                    "isin_div_payout": fields[1] if fields[1] != "-" else "NA",
                    "isin_div_reinvestment": fields[2] if fields[2] != "-" else "NA",
                    "scheme_name": fields[3],
                    "net_asset_value": fields[4],
                    "date": fields[5],
                }

                # Check if a record with the same scheme_code already exists
                existing_record = collection.find_one(
                    {"scheme_code": record_dict["scheme_code"]}
                )

                if existing_record is None:
                    # If no existing record, insert a new document with nav_data array
                    collection.insert_one(
                        {
                            "scheme_type": record_dict["scheme_type"],
                            "fund_house": record_dict["fund_house"],
                            "scheme_code": record_dict["scheme_code"],
                            "isin_div_payout": record_dict["isin_div_payout"],
                            "isin_div_reinvestment": record_dict[
                                "isin_div_reinvestment"
                            ],
                            "scheme_name": record_dict["scheme_name"],
                            "nav_data": [
                                {
                                    "net_asset_value": record_dict["net_asset_value"],
                                    "date": record_dict["date"],
                                }
                            ],
                        }
                    )
                else:
                    # If an existing record, check if the date already exists in nav_data
                    existing_dates = [
                        entry["date"] for entry in existing_record.get("nav_data", [])
                    ]
                    if record_dict["date"] not in existing_dates:
                        # Append the new NAV data to the nav_data array if date doesn't exist
                        collection.update_one(
                            {"_id": existing_record["_id"]},
                            {
                                "$push": {
                                    "nav_data": {
                                        "net_asset_value": record_dict[
                                            "net_asset_value"
                                        ],
                                        "date": record_dict["date"],
                                    }
                                }
                            },
                        )

                record_count += 1
        client.close()
        print(f"Total records added: {record_count}")
        print("Process complete")

    except Exception as e:
        print(f"An error occurred: {str(e)}")


# Load environment variables
load_dotenv()

# Load lists from files
fund_houses = load_list_from_file(FUND_HOUSE_FILE_PATH)
scheme_types = load_list_from_file(SCHEME_TYPE_FILE_PATH)

if __name__ == "__main__":
    start_time = time.time()
    fetch_and_insert_data()
    end_time = time.time()

    print(f"Total execution time: {end_time - start_time} seconds")
