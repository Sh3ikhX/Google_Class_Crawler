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
sql = "SELECT * FROM courses"
mycursor.execute(sql)
myresult = mycursor.fetchall()
# for x in myresult:
#   if(x[3]==0 orx[4]==0 or x[5]==0)


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