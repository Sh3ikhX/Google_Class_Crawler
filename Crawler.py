from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import re
from video_metadata import videodata

from db import mycursor, mydb
import datetime

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/classroom.student-submissions.students.readonly',
          'https://www.googleapis.com/auth/classroom.courses.readonly',
          'https://www.googleapis.com/auth/classroom.courseworkmaterials'
          ]

lectures = assingnments = mid_exam = final_exam = 0


def main():
    """Shows basic usage of the Classroom API.
    Prints the names of the first 10 courses the user has access to.
    """
    global x
    x = datetime.datetime.now()
    mycursor.execute("TRUNCATE courses")
    mycursor.execute("TRUNCATE video_details")

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

    courses_api = service.courses().list(pageSize=1000).execute()
    courses = courses_api.get('courses', [])

    global courseid

    courseid = []

    if not courses:
        print('No courses found.')
    else:
        for course in courses:
            print("*******************************")
            print("Course Name: " + course['name'])
            courseid.append(course['id'])
            materials_api = service.courses().courseWork().list(courseId=course['id']).execute()
            materials = materials_api.get('courseWork', [])
            print(materials)
            material_print(materials, course['name'], course['id'])

    mydb.commit()
    print("\n\n==================================\n\n\t\tCrawling Completed\n\n==================================\n\n")
    print("Do you want to print the Database?")
    ans = input("Press Y to continue Or N to Quit = ")

    if ("y" in ans or "Y" in ans):
        print_db()
    else:
        quit()


def print_db():
    sql = "SELECT * FROM courses INNER JOIN video_details ON courses.course_id = video_details.course_id ORDER BY courses.coursename"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    print("CourseName\t\t\t CourseID\t\t Lectures  Assignments  MIDs  Finals  VideoDuration ")
    for x in myresult:
        print("%-20s" % (x[1]), x[2], "%6s" % (x[3]), "%10s" % (x[4]), "%10s" % (x[5]), "%5s" % (x[6]),
              "%10s" % (x[10]))


def material_print(materials, name, c_id):
    global imagecount
    global videocount
    global pdfcount
    global word
    global ppt
    global excel
    imagecount = videocount = pdfcount =excel=ppt= word=0
    global lectures
    global assingnments
    global mid_exam
    global final_exam

    if not materials:
        print('No material found.')
    else:
        print('\nMaterials Type And Count:')
        for material in materials:

            classification(material['title'])
            try:
                for i in material['materials']:
                    form = (i['driveFile']["driveFile"]['title'])
                    id = (i['driveFile']["driveFile"]['id'])
                    imagecount += form_images(form, c_id)
                    videocount += form_videos(form, id, c_id)
                    pdfcount += form_pdf(form, c_id)
                    word+= form_word(form, c_id)
                    ppt+= form_ppt(form, c_id)
                    excel+= form_excel(form, c_id)
            except:
                print("\nNO material found in " + material['title'])

    print("\n\n\nclass id = " + str(c_id))
    print("\n\nImages = " + str(imagecount))
    print("Videos = " + str(videocount))
    print("Pdf = " + str(pdfcount))
    print("Word Files = " + str(word))
    print("PPT Files = " + str(ppt))
    print("Excel Files = " + str(excel))
    print("\nClassification: ")
    print("Total Lectures = " + str(lectures) + "\nTotal Assignments  = " + str(
        assingnments) + "\nTotal Mid exams = " + str(mid_exam) + "\nTotal Final exam = " + str(final_exam))

    sql = "INSERT INTO courses (coursename, course_id,lectures,assignments,mid_exams,final_exam) VALUES (%s, %s,%s, %s,%s, %s)"
    val = (name, str(c_id), str(lectures), str(assingnments), str(mid_exam), str(final_exam))

    mycursor.execute(sql, val)

    sql = "UPDATE video_details SET image_count = %s,video_count = %s,pdf_count = %s WHERE course_id = %s"
    val = (str(imagecount),str(videocount),str(pdfcount),str(c_id))

    mycursor.execute(sql, val)

    lectures = assingnments = mid_exam = final_exam = 0




def form_word(form, c_id):
    if ((re.findall(r"\S+\.docx", form)) or re.findall(r"\S+\.doc", form)):
        return 1
    else:
        return 0


def form_ppt(form, c_id):
    if ((re.findall(r"\S+\.pptx", form)) or re.findall(r"\S+\.ppt", form)):
        return 1
    else:
        return 0


def form_excel(form, c_id):
    if ((re.findall(r"\S+\.xlsx", form)) or re.findall(r"\S+\.xls", form)):
        return 1
    else:
        return 0


def form_images(form, c_id):
    if ((re.findall(r"\S+\.jpg", form)) or re.findall(r"\S+\.png", form)):
        sql = "INSERT INTO video_details (course_id,image_title) VALUES (%s,%s)"
        val = (str(c_id), form)
        mycursor.execute(sql, val)
        return 1
    else:
        return 0


def form_videos(form, id, c_id):
    # print()
    if ((re.findall(r"\S+\.mp4", form))):
        print("Title = " + form)
        data = videodata(id)
        print("Duration = " + str(data) + ' seconds')
        sql = "INSERT INTO video_details (course_id,video_title,video_duration) VALUES (%s, %s,%s)"
        val = (str(c_id), str(form), str(data))
        mycursor.execute(sql, val)
        return 1
    else:
        return 0


def form_pdf(form, c_id):
    if ((re.findall(r"\S+\.pdf", form))):
        sql = "INSERT INTO video_details (course_id,pdf_title) VALUES (%s, %s)"
        val = (str(c_id), form)
        mycursor.execute(sql, val)
        return 1
    else:
        return 0


def classification(title):
    global lectures
    global assingnments
    global mid_exam
    global final_exam

    if ("Lecture" in title or "lecture" in title):
        lectures += 1
    elif ("assignment" in title or "Assignment" in title):
        assingnments += 1
    elif ("Mid exam" in title or "Mid term" in title or "mid Term" in title or "mid" in title or "Mid" in title):
        mid_exam += 1
    elif (
            "Final exam" in title or "Final term" in title or "final Term" in title or "Final" in title or "final" in title):
        final_exam += 1


if __name__ == '__main__':
    main()
