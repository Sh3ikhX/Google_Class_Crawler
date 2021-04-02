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

