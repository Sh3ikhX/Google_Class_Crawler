from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/classroom.student-submissions.me.readonly ",
          "https://www.googleapis.com/auth/classroom.student-submissions.students.readonly"
          ]


def main():
    """Shows basic usage of the Classroom API.
    Prints the names of the first 10 courses the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
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
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('classroom', 'v1', credentials=creds)

    # Call the Classroom API
    results = service.courses().list(pageSize=100).execute()
    # courses = results.get('courses', [])
    work = results.get('CourseWork', [])

    # if not courses:
    #     print('No courses found.')
    # else:
    #     print('Courses:')
    #     for course in courses:
    #         #print(course['name']+" ID: "+course['id'])
    #         print(course)

    if not work:
        print('No work found.')
    else:
        print('Work:')
        for works in work:
            # print(course['name']+" ID: "+course['id'])
            print(works)
    # for


if __name__ == '__main__':
    main()
