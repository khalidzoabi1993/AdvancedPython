import mysql.connector
mydb = mysql.connector.connect(host='localhost',
                               user='root',
                               password='admin')
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS mydatabase")
# mycursor.execute("SHOW DATABASES")
# for x in mycursor:
#   print(x)
mycursor.execute("use mydatabase")
# mycursor.execute("CREATE TABLE IF NOT EXISTS KHALIDTESTTABLE (name VARCHAR(255), address VARCHAR(255))")
mycursor.execute("INSERT INTO KHALIDTESTTABLE (name, address) VALUES ('John', 'Highway 21')")
# mycursor.execute("SELECT * FROM students_db.students")
# mycursor.execute("use mydatabase")
# mycursor.execute("CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))")