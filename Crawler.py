from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import re

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/classroom.student-submissions.students.readonly',
          'https://www.googleapis.com/auth/classroom.courses.readonly',
          'https://www.googleapis.com/auth/classroom.courseworkmaterials'

          ]
# https://www.googleapis.com/auth/classroom.courses.readonly
# https://www.googleapis.com/auth/classroom.coursework.students.readonly




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
    #results2 = service.courses().courseWork().list(courseId="308463026162").execute()
    #work = results2.get('courseWork', [])
    courses_api = service.courses().list(pageSize=100).execute()
    #materials_api = service.courses().courseWorkMaterials().list(courseId="308463026162").execute()


    courses = courses_api.get('courses', [])
   # materials = materials_api.get('courseWorkMaterial', [])
    #print(materials_api)

    if not courses:
        print('No courses found.')
    else:
        #print('Courses:')
        for course in courses:
            print("*******************************")
            print("Course Name: "+course['name'])
            materials_api = service.courses().courseWorkMaterials().list(courseId=course['id']).execute()
            materials = materials_api.get('courseWorkMaterial', [])
            material_print(materials)
            #print("*******************************")



def material_print(materials):
    imagecount = videocount = pdfcount = 0

    if not materials:
        print('No material found.')
    else:
        print('\nMaterials Type And Count:')
        for material in materials:
            print(material['materials'])
            for i in material['materials']:
                # print(i['driveFile']["driveFile"]['title'])
                form = (i['driveFile']["driveFile"]['title'])
                # imagecount += form_images(form)
                # videocount += form_videos(form)
                # pdfcount += form_pdf(form)

    print("Images = " + str(imagecount))
    print("Videos = " + str(videocount))
    print("Pdf = " + str(pdfcount))

def form_images(form):
    if ((re.findall(r"\S+\.jpg", form)) or re.findall(r"\S+\.png", form)):
        return 1
    else:
        return 0


def form_videos(form):
    if ((re.findall(r"\S+\.mp4", form))):
        return 1
    else:
        return 0


def form_pdf(form):
    if ((re.findall(r"\S+\.pdf", form))):
        return 1
    else:
        return 0






if __name__ == '__main__':
    main()