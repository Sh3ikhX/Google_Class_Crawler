from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly','https://www.googleapis.com/auth/drive.appdata']
creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token1.json'):
    creds = Credentials.from_authorized_user_file('token1.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'drive.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token1.json', 'w') as token:
            token.write(creds.to_json())

service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API

videoID='1sT2pWeGZ8yfJSRHyTOYH04YCjLGaYiNb'



def videodata(videoID):
        results1 = service.files().get(fileId=videoID,fields='videoMediaMetadata').execute()
        data = (results1['videoMediaMetadata']['durationMillis'])
        seconds = int(data) / 1000
        return (seconds)

