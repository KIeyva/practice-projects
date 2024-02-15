import mysql.connector
from mysql.connector import Error

#create a connection function
'''Obtained sql functions from notes'''
def create_con(hostname, uname, passwd, dbname):
    connection = None

    try:
        connection  = mysql.connector.connect(
            host = hostname,
            user = uname,
            password = passwd,
            database = dbname
        )
        print('Connection is successful')
    except Error as e:
        print('Connection failed with error:', e)
    return connection

#execute a query in DB (insert, update, delete)
def execute_myquery(connection, query):
    mycursor = connection.cursor()
    try: 
        mycursor.execute(query)
        connection.commit()
        print("Query is successful")
    except Error as e:
        print("Error: ", e)

#execute a query to read from DB (select statement)
def execute_read_myquery(connection, query):
    mycursor = connection.cursor(dictionary=True)
    rows = None
    try:
        mycursor.execute(query)
        rows = mycursor.fetchall()
        return rows
    except Error as e:
        print("Error is :", e)