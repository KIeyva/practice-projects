import mysql.connector
from mysql.connector import Error

import creds

from sql import create_con
from sql import execute_myquery
from sql import execute_read_myquery

#connection to database
mycreds = creds.creds()
con = create_con(mycreds.hostname, mycreds.username, mycreds.password, mycreds.database)

#create a new table
# sql = "create table floor(id int not null auto_increment, level int(3), name varchar(20), PRIMARY KEY (id));"
# execute_myquery(con, sql)
# sql = "create table room(id int not null auto_increment, capacity int(4), number int(4), floor int, FOREIGN KEY (floor) REFERENCES floor(id), PRIMARY KEY (id));"
# execute_myquery(con, sql)
# sql = "create table resident(id int not null auto_increment, f_name varchar(20), l_name varchar(20), age int(3), room int, FOREIGN KEY (room) REFERENCES room(id), PRIMARY KEY (id));"
# execute_myquery(con, sql)

# #update table
# sql = 'ALTER TABLE room auto_increment=100;'
# execute_myquery(con, sql)
# sql = 'ALTER TABLE resident auto_increment=5000;'
# execute_myquery(con, sql)
# insert into floor table
# sql = ('insert into floor(level, name) values '
#     '(-5, "Black"),'
#     '(-4, "Gray"),'
#     '(-3, "White"),'
#     '(-2, "Brown"),'
#     '(-1,"Green"),'
#     '(0, "Lobby"),'
#     '(1, "Orange"),'
#     '(2,"Red"),'
#     '(3, "Violet"),'
#     '(4, "Purple"),'
#     '(5, "Blue"),'
#     '(6, "Yellow"),'
#     '(7, "Pink")')  

# insert into room table
# sql = ('insert into room(capacity, number, floor) values'
#        '(4, -500, 1),'
#        '(5, -501, 1),'
#        '(4, -502, 1),'
#        '(4, -400, 2),'
#        '(8, -401, 2),'
#        '(5, -402, 2),'
#        '(2, -300, 3),'
#        '(2, -301, 3),'
#        '(2, -302, 3),'
#        '(4, -200, 4),'
#        '(4, -201, 4),'
#        '(4, -100, 5),'
#        '(10, -101, 5),'
#        '(100, 0, 6),'
#        '(100, 1, 6),'
#        '(30, 2, 6),'
#        '(10, 100, 7),'
#        '(10, 101, 7),'
#        '(2, 102, 7),'
#        '(10, 200, 8),'
#        '(6, 201, 8),'
#        '(16, 202, 8),'
#        '(10, 300, 9),'
#        '(4, 301, 9),'
#        '(4, 302, 9),'
#        '(4, 303, 9),'
#        '(4, 400, 10),'
#        '(6, 401, 10),'
#        '(6, 402, 10),'
#        '(16, 500, 11),'
#        '(10, 501, 11),'
#        '(4, 502, 11),'
#        '(4, 600, 12),'
#        '(10, 601, 12),'
#        '(4, 602, 12),'
#        '(8, 700, 13),'
#        '(10, 701, 13),'
#        '(8, 702, 13)')

# # insert into resident table
# sql = ('insert into resident(f_name, l_name, age, room) values'
#        '("Mike", "Jones", 71, 1),'
#        '("Jane", "Doe", 85, 5),'
#        '("Donna", "Smith", 74, 10),'
#        '("Ricky", "Smith", 80, 3),'
#        '("John", "Deer", 93, 9)')

# execute_myquery(con, sql)