from __future__ import print_function
import datetime
import os.path
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token_bak.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly', 'https://www.googleapis.com/auth/drive.file']



def check_date():
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    import creddy

    # Define the necessary scopes
    SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
    """Shows basic usage of the Drive v3 API.
            Prints the names and ids of the first 10 files the user has access to.
            """
    creds = None
    import creddy
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



    # Build the Drive API service
    service = build('drive', 'v3', credentials=creds)

    # Specify the file ID of the file you want to check
    file_id = '1haSp-9dS0qX4PfchW1LgC35M8bxOw62Y'

    try:
        # Retrieve the file metadata
        file_metadata = service.files().get(fileId=file_id, fields='modifiedTime').execute()

        # Get the 'modifiedTime' property from the file metadata
        modified_time = file_metadata['modifiedTime']

        print(f"Last modified time of the file: {modified_time}")
        return modified_time



    except Exception as e:
        print(f"An error occurred: {e}")


def list_files():
    """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
    creds = None
    import creddy
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

    try:
        service = build('drive', 'v3', credentials=creds)

        # Call the Drive v3 API
        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
            return
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')

def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    import creddy
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

    try:
        service = build('drive', 'v3', credentials=creds)
        file_path = 'game_collection.xlsx'
        folder_id = '19NgV-i6PCT4OnSAotEUkNuj8pMRmUmdN'
        # Create a file metadata
        file_metadata = {
            'name': os.path.basename(file_path),
            'parents': [folder_id],  # Optional: specify the folder where you want to upload
        }

        existing_files = service.files().list(q="name = 'game_collection.xlsx'").execute()
        if 'files' in existing_files and len(existing_files['files']) > 0:
            print("File exists, updating.")
            file_id = existing_files['files'][0]['id']
            media = MediaFileUpload(file_path,
                                    mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            updated_file = service.files().update(fileId=file_id, media_body=media).execute()
            print('File ID:', updated_file.get('id'))
        else:
            print("File not found on Google Drive.")
            print("Uploading File")
            # Upload the file
            media = MediaFileUpload(file_path, resumable=True)
            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()

            print(f'File ID: {file["id"]}')

            list_files()
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    #main()
    check_date()


# Find the existing file by name




