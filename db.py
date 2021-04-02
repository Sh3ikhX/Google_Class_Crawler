import mysql.connector

try:
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="$h3!khX",
    database = "crawler"
  )
except Exception as e:
    print('Not connected')

print(mydb)
mycursor = mydb.cursor()
sql="SELECT * FROM courses INNER JOIN video_details ON courses.course_id = video_details.course_id ORDER BY courses.id"
mycursor.execute(sql)
myresult = mycursor.fetchall()
for x in myresult:
  print(x)
#
# sql = "INSERT INTO courses (coursename, course_id) VALUES (%s, %s)"
# val = (str("course['name']"), "course['id']")
# mycursor.execute(sql, val)
#
# mycursor.execute("SELECT * FROM courses")
#
# myresult = mycursor.fetchall()
#
# for x in myresult:
#   print(x)


# mydb.commit()
# mycursor.execute("SHOW TABLES")
#
# for x in mycursor:
#   print(x)