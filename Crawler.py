from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import re
from video_metadata import videodata
import xlwt
from db import mycursor,mydb

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/classroom.student-submissions.students.readonly',
          'https://www.googleapis.com/auth/classroom.courses.readonly',
          'https://www.googleapis.com/auth/classroom.courseworkmaterials'

          ]
# https://www.googleapis.com/auth/classroom.courses.readonly
# https://www.googleapis.com/auth/classroom.coursework.students.readonly


lectures = assingnments = mid_exam = final_exam = 0

def main():
    """Shows basic usage of the Classroom API.
    Prints the names of the first 10 courses the user has access to.
    """
    global file1
    file1 = open("MyFile.txt", "w")


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





    # global coursename
    global courseid
    # coursename = []
    courseid = []

    if not courses:
        print('No courses found.')
    else:
        #print('Courses:')
        for course in courses:
            print("*******************************")
            print("Course Name: "+course['name'])
            file1.write("\n*******************************\nCourse Name: "+course['name'])
            # coursename.append(course['name'])
            courseid.append(course['id'])

            # sql = "INSERT INTO courses (coursename, course_id) VALUES (%s, %s)"
            # val = (course['name'],course['id'])
            # mycursor.execute(sql, val)
            materials_api = service.courses().courseWorkMaterials().list(courseId=course['id']).execute()

            # sql = "INSERT INTO courses (coursename, course_id) VALUES (%s, %s)"
            # val = (str(course['name']), course['id'])
            # mycursor.execute(sql, val)

            materials = materials_api.get('courseWorkMaterial', [])
            material_print(materials,course['name'],course['id'])
            #print("*******************************")
    #print(len(coursename))
   # report()
   #  for c in coursename:
   #      # print(c)
   #      i=0
   #      # print(courseid[i])
   #
   #      sql = "INSERT INTO courses (coursename, course_id,lectures,assignments,mid_exams,final_exam) VALUES (%s, %s,%s, %s,%s, %s)"
   #      val = (str(c), courseid[i],lectures,assingnments,mid_exam,final_exam)
   #      mycursor.execute(sql, val)
   #      i += 1

    mydb.commit()

    print('\n\n=============================\npriting from db')
    sql="SELECT * FROM courses INNER JOIN video_details ON courses.course_id = video_details.course_id ORDER BY courses.id"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    columns = mycursor.description
    result = [{columns[index][0]: column for index, column in enumerate(value)} for value in mycursor.fetchall()]
    print(result)
    for x in myresult:
        print(x)
    file1.close()


def material_print(materials,name,c_id):
    global imagecount
    global videocount
    global pdfcount
    imagecount = videocount = pdfcount = 0
    global lectures
    global assingnments
    global mid_exam
    global final_exam
    global mat_title
    mat_title=[]



    if not materials:
        print('No material found.')
    else:
        print('\nMaterials Type And Count:')
        for material in materials:
            #print(material['materials'])

            classification(material['title'])
            for i in material['materials']:
                # print(i['driveFile']["driveFile"]['title'])
                form = (i['driveFile']["driveFile"]['title'])
                mat_title.append(i['driveFile']["driveFile"]['title'])
                id = (i['driveFile']["driveFile"]['id'])
                imagecount += form_images(form,c_id)
                videocount += form_videos(form,id,c_id)
                pdfcount += form_pdf(form,c_id)
    #print("***************************\nStats")

    print("\n\n\nclass id = "+str(c_id))
    print("\n\nImages = " + str(imagecount))
    print("Videos = " + str(videocount))
    print("Pdf = " + str(pdfcount))
    print("\nClassification: ")
    print("Total Lectures = " + str(lectures) + "\nTotal Assignments  = " + str(
        assingnments) + "\nTotal Mid exams = " + str(mid_exam) + "\nTotal Final exam = " + str(final_exam))



    file1.write("\n\nClassification: "+"\nTotal Lectures = " + str(lectures) + "\nTotal Assignments  = " + str(
        assingnments) + "\nTotal Mid exams = " + str(mid_exam) + "\nTotal Final exam = " + str(final_exam))

    file1.write("\n\nFile Types And Count\nImages = " + str(imagecount) + "\nVideos = " + str(videocount) + "\nPdf = " + str(pdfcount))

    sql = "INSERT INTO courses (coursename, course_id,lectures,assignments,mid_exams,final_exam) VALUES (%s, %s,%s, %s,%s, %s)"
    val = (name, str(c_id), str(lectures), str(assingnments), str(mid_exam), str(final_exam))
    mycursor.execute(sql, val)
    lectures = assingnments = mid_exam = final_exam = 0





def form_images(form,c_id):
    if ((re.findall(r"\S+\.jpg", form)) or re.findall(r"\S+\.png", form)):
        sql = "INSERT INTO video_details (course_id,image_title) VALUES (%s, %s)"
        val = (str(c_id), form)
        mycursor.execute(sql, val)
        return 1
    else:
        return 0


def form_videos(form,id,c_id):
    #print()
    if ((re.findall(r"\S+\.mp4", form))):
        print("Title = "+form)
        #print("id = "+id)
        data = videodata(id)
        print("Duration = "+str(data)+' seconds')
        file1.write("\nTitle of video = "+form+"\nDuration = "+str(data)+' seconds')
        sql="INSERT INTO video_details (course_id,video_title,video_duration) VALUES (%s, %s,%s)"
        val = (str(c_id), str(form), str(data))
        mycursor.execute(sql, val)
        return 1
    else:
        return 0


def form_pdf(form,c_id):
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
    #lectures = assingnments = mid_exam = final_exam = 0

    if("Lecture" in title or "lecture" in title):
        lectures+=1
    elif("assignment " in title or "Assignment " in title):
        assingnments+=1
    elif ("Mid exam" in title or "Mid term" in title or "mid Term" in title or "mid" in title or "Mid" in title):
        mid_exam += 1
    elif ("Final exam" in title or "Final term" in title or "final Term" in title or "Final" in title or "final" in title):
        final_exam += 1








if __name__ == '__main__':
    main()