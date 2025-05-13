import mysql.connector

connection = mysql.connector.connect(host="localhost", user="root", password="",database="python_db")

if connection.is_connected():
    print("connected successfully")
else:
    print("failed to connect")

connection.close()