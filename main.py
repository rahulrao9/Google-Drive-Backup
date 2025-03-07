import os
import time
import logging
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from google.oauth2 import service_account
import json
import io

# Set up logging
current_directory = os.getcwd()
logs_dir = os.path.join(current_directory, 'backup/logs')
logs_file = os.path.join(logs_dir, 'backup.log')

# Ensure logs directory exists
os.makedirs(logs_dir, exist_ok=True)

logging.basicConfig(filename=logs_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

SCOPES = ["https://www.googleapis.com/auth/drive"]
SERVICE_ACCOUNT_FILE = "credentials.json"
PARENT_FOLDER_ID = "166bz8k9oRIuqhiGIz8a3HA48qlMRW8Jf"

def authenticate():
    with open(SERVICE_ACCOUNT_FILE, 'r') as f:
        service_account_info = json.load(f)
    creds = service_account.Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
    return creds

def check_file_in_drive(file_name):
    creds = authenticate()
    service = build("drive", "v3", credentials=creds)

    # Check if the file exists in the parent folder
    results = service.files().list(q=f"name='{file_name}' and '{PARENT_FOLDER_ID}' in parents and trashed=false", fields="files(id)").execute()
    files = results.get('files', [])

    # If file not found in Drive, return True indicating file is not present
    return not files

def upload_file(file_path):
    creds = authenticate()
    service = build("drive", "v3", credentials=creds)

    file_name = os.path.basename(file_path)

    try:
        # Check if the file is already present in Drive
        if check_file_in_drive(file_name):
            file_metadata = {
                'name': file_name,
                'parents': [PARENT_FOLDER_ID]
            }

            media = MediaFileUpload(file_path, resumable=True)

            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()

            logging.info(f"Uploaded '{file_name}' successfully.")
            print(f"Uploaded '{file_name}' successfully.")
        else:
            logging.info(f"File '{file_name}' already exists in Drive.")
            print(f"File '{file_name}' already exists in Drive.")
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        print(f"Error occurred: {e}")

def upload_files_in_folder():
    logging.info("Current directory: %s", current_directory)
    print("Current directory:", current_directory)

    # List files in the current directory
    logging.info("Files in the current directory:")
    print("Files in the current directory:")
    for filename in os.listdir(current_directory):
        logging.info(filename)
        print(filename)

    # List files in the 'data' directory
    data_directory = os.path.join(current_directory, 'backup/files')
    logging.info("Files in the 'data' directory:")
    print("Files in the 'data' directory:")
    for filename in os.listdir(data_directory):
        logging.info(filename)
        print(filename)

    folder_path = os.path.join(current_directory, 'backup/files')
    logging.info("Input folder path: %s", folder_path)
    print("Input folder path:", folder_path)
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            logging.info("Uploading file: %s", file_name)
            print("Uploading file:", file_name)
            file_path = os.path.join(root, file_name)
            upload_file(file_path)

# Call the function to start the backup process
upload_files_in_folder()
logging.info("Backup process completed.")
print("Backup process completed.")

def write_hello_world_file_to_drive():
    # Define the content of the text file
    content = "Hello, World!"

    # Define the file name
    file_name = "hello_world.txt"

    try:
        # Authenticate with Google Drive
        creds = authenticate()
        service = build("drive", "v3", credentials=creds)

        # Check if the file already exists in Drive
        if check_file_in_drive(file_name):
            # Create file metadata
            file_metadata = {
                'name': file_name,
                'parents': [PARENT_FOLDER_ID]
            }

            # Create a MediaIoBaseUpload object with the content
            media = MediaFileUpload(io.BytesIO(content.encode()), mimetype='text/plain', resumable=True)

            # Upload the file
            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()

            logging.info(f"Uploaded '{file_name}' successfully.")
            print(f"Uploaded '{file_name}' successfully.")
        else:
            logging.info(f"File '{file_name}' already exists in Drive.")
            print(f"File '{file_name}' already exists in Drive.")
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        print(f"Error occurred: {e}")

# Call the function to write and upload the "Hello World" text file
# write_hello_world_file_to_drive()