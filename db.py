import mysql.connector


mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="$h3!khX",
        database="crawler"
)

mycursor = mydb.cursor()
