import os
import datetime
import pytz
import shutil
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from io import FileIO
import gdrive_upload
import creddy
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# Specify the folder where you want to store backups
BACKUP_FOLDER = 'backups'

# Function to check and perform synchronization
def gdrive_sync():
    # Get the last modified time of the Google Drive file as a string
    gdrive_date_str = gdrive_upload.check_date()

    # Convert the string to a datetime object and set it to UTC timezone
    gdrive_date_time = datetime.datetime.fromisoformat(gdrive_date_str).astimezone(pytz.UTC)

    # Specify the filename of the local file you want to check
    filename = 'game_collection.xlsx'

    try:
        # Get the last modified time of the local file and set it to UTC timezone
        local_modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(filename), tz=pytz.UTC)

        # Compare the two timestamps
        time_difference = gdrive_date_time - local_modified_time

        if time_difference.total_seconds() > 0:
            print("The Google Drive file is newer than the local file.")

            # Create the backup folder if it doesn't exist
            if not os.path.exists(BACKUP_FOLDER):
                os.makedirs(BACKUP_FOLDER)

            # Create a backup of the local file with a timestamp in the filename
            backup_filename = os.path.join(BACKUP_FOLDER, f'game_collection_bak_{local_modified_time.strftime("%Y%m%d_%H%M%S")}.xlsx')
            shutil.copy(filename, backup_filename)

            print(f"Backup created: {backup_filename}")

            # Download the Google Drive file and replace the local file
            download_and_replace(filename)

        elif time_difference.total_seconds() < 0:
            print("The local file is newer than the Google Drive file.")
        else:
            print("The files have the same last modified time.")

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Function to download the Google Drive file and replace the local file
def download_and_replace(filename):
    try:

        # Initialize Google Drive API
        SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
        cred_file = creddy.client_secret
        # The file token_bak.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    cred_file, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        service = build('drive', 'v3', credentials=creds)

        # Replace 'your-file-id' with the actual file ID of your Google Drive file
        file_id = '1haSp-9dS0qX4PfchW1LgC35M8bxOw62Y'

        # Download the Google Drive file
        request = service.files().get_media(fileId=file_id)
        fh = FileIO(filename, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}%.")

        print(f"Downloaded Google Drive file: {filename}")
    except Exception as e:
        print(f"An error occurred during download: {e}")

if __name__ == '__main__':
    gdrive_sync()
