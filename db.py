import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="$h3!khX",
  database = "crawler"
)

print(mydb)
mycursor = mydb.cursor()


# sql = "INSERT INTO courses (id,coursename, course_id) VALUES (%s,%s, %s)"
# val = (0,str("course['name']"), "course['id']")
# mycursor.execute(sql, val)
#
# mycursor.execute("SELECT * FROM courses")
#
# myresult = mycursor.fetchall()
#
# for x in myresult:
#   print(x)
# mycursor.execute("SHOW TABLES")
#
# for x in mycursor:
#   print(x)