# main.py
from modules.fetch_nav_data import fetch_nav_data
from modules.upload_nav_data import upload_nav_data
from modules.fetch_and_insert_data import fetch_and_insert_data

def main():
    fetch_nav_data()
    upload_nav_data()
    fetch_and_insert_data()

if __name__ == "__main__":
    main()
