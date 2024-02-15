#create flask api
import flask
from flask import jsonify
from flask import request, make_response


from sql import create_con
from sql import execute_myquery
from sql import execute_read_myquery

import creds
import hashlib
import datetime
import time
#create application and its set up

app  = flask.Flask(__name__)
app.config['DEBUG'] = True #for the purpose of seeing errors in browser

master_username = 'Kevin'
master_password = '1cf3f9b6ce57cf0dc36a5a96ad517ffc12221726161ca6768632f4ef568788a9'
# master password: passwordisharris
@app.route('/auth', methods=['GET'])
def process_request():
    if request.authorization:
        encodedpasswd = request.authorization.password.encode() #gettign password in unicode values
        hashvalue = hashlib.sha256(encodedpasswd)
        if request.authorization.username == master_username and hashvalue.hexdigest() == master_password:
            return '<h1> Authenticated User </h1>'
    return make_response('Could not find user', 401, {'WWW-Authenticate:': 'Basic realm="Login Required"'})


#default route with GET method
@app.route("/", methods=['GET'])
def defaultmsg():
    return "<h1> Hello World </h1>"
'''Obtained lines 1-21 from notes'''

"""This block contains all pages GET all routes"""

@app.route("/api/floor/view/all", methods=['GET'])
def view_floors_all():
    my_creds = creds.creds()
    con = create_con(my_creds.hostname, my_creds.username, my_creds.password, my_creds.database)
    sql = "select level, name from floor"
    content = execute_read_myquery(con, sql)
    return jsonify(content)

@app.route("/api/room/view/all", methods=['GET'])
def view_room_all():
    my_creds = creds.creds()
    con = create_con(my_creds.hostname, my_creds.username, my_creds.password, my_creds.database)
    sql = ("select room.capacity, room.number, floor.level as floor from room "
           "inner join floor on room.floor=floor.id;") #sql statement that replaces foreign key with value in other table, hiding it from user
    content = execute_read_myquery(con, sql)
    
    return jsonify(content)

@app.route("/api/resident/view/all", methods=['GET'])
def view_resident_all():
    my_creds = creds.creds()
    con = create_con(my_creds.hostname, my_creds.username, my_creds.password, my_creds.database)
    sql = ("select resident.f_name, resident.l_name, resident.age, room.number as room from resident "
           "inner join room on resident.room=room.id") #sql statement that replaces foreign key with value in other table, hiding it from user
    content = execute_read_myquery(con, sql)
    return jsonify(content)

"""This block contains all pages GET all routes"""


"""This block contains all pages individual GET routes"""
@app.route("/api/floor/view", methods=['GET'])
def view_floor():
    target_id = request.args.get('level') #assuming every input is correct, will read level input
    
    my_creds = creds.creds()
    con = create_con(my_creds.hostname, my_creds.username, my_creds.password, my_creds.database)
    sql = f"select level, name from floor where level='{target_id}'" #sql statment with condition
    floor = execute_read_myquery(con, sql)
    return jsonify(floor)    

@app.route("/api/room/view", methods=['GET'])
def view_room():
    target_id = request.args.get('room')
    
    my_creds = creds.creds()
    con = create_con(my_creds.hostname, my_creds.username, my_creds.password, my_creds.database)
    sql = (f"select room.capacity, room.number, floor.level as floor from room "
           f"inner join floor on room.floor=floor.id where room.number='{target_id}'") #selecting specific record whilst hiding foreign key with replacement value
    room = execute_read_myquery(con, sql)
    return jsonify(room)  

@app.route("/api/resident/view", methods=['GET'])
def view_resident():   
    # record is searchable by having both first and last name
    target_f = request.args.get('f_name')
    target_l = request.args.get('l_name')

    #TODO: add ability to search by first OR last name and display all results
    my_creds = creds.creds()
    con = create_con(my_creds.hostname, my_creds.username, my_creds.password, my_creds.database)
    
    #selecting specific record whilst hiding foreign key with replacement value
    sql = (f"select resident.f_name, resident.l_name, resident.age, room.number as room from resident "
           f"inner join room on resident.room=room.id WHERE resident.f_name='{target_f}' and resident.l_name='{target_l}'")
    resident = execute_read_myquery(con, sql)
    return jsonify(resident) 
"""This block contains all pages individual GET routes"""


"""This block contains all pages POST routes"""
@app.route("/api/floor", methods=['POST'])
def floor_insert():
    levels = []
    names = []
    my_creds = creds.creds()
    con = create_con(my_creds.hostname, my_creds.username, my_creds.password, my_creds.database)
    sql = "select level, name from floor"
    floors = execute_read_myquery(con, sql)
    
    for record in floors: #store all taken levels for checking
        levels.append(record['level'])
    for record in floors: #store all taken levels for checking
        names.append(record['name'])
        
    request_data = request.get_json() #taking new values for inserting
    new_level = request_data['level']
    new_name = request_data['name']
    
    if request_data['level'] in levels or request_data['name'] in names: #value check for existing values
        return 'Error: floor level or name already exists.'
    else:
        sql2 = (f'insert into floor(level, name) values'
                f'({new_level}, "{new_name}")')
        execute_myquery(con, sql2)
        return f'Floor level:{new_level} ({new_name}) successfully added.'

@app.route("/api/room", methods=['POST'])
def room_insert():
    numbers = []

    my_creds = creds.creds()
    con = create_con(my_creds.hostname, my_creds.username, my_creds.password, my_creds.database)  
    sql = ("select room.number, floor.level from room "
           "left join floor on room.floor = floor.id")
    rooms = execute_read_myquery(con, sql)
    sql2 = "select * from floor"
    floors = execute_read_myquery(con, sql2)
    
    for record in rooms:
        numbers.append(record['number'])
    
    request_data = request.get_json() #taking new values for inserting
    new_capacity = int(request_data['capacity'])
    new_number = int(request_data['number'])
    new_floor = int(request_data['floor'])
    real_floor = 0
    
    for record in floors:
        if record['level'] == new_floor:
            real_floor = record['id']
    
    if request_data['number'] not in numbers: #value check for existing values
        sql3 = (f"insert into room(capacity, number, floor) values"
                f"({new_capacity}, {new_number}, {real_floor})")
        execute_myquery(con, sql3)
        return f"Room number:{new_number} on floor:{new_floor} successfully added."
    else:
        return 'Error: room number already exists.'
    
@app.route("/api/resident", methods=['POST'])
def resident_insert():

    my_creds = creds.creds()
    con = create_con(my_creds.hostname, my_creds.username, my_creds.password, my_creds.database)  
    sql = ("select resident.f_name, resident.l_name, resident.age, room.number as room from resident "
           "left join room on resident.room = room.id")
    residents = execute_read_myquery(con, sql)
    sql2 = "select * from room"
    rooms = execute_read_myquery(con, sql2)

    
    request_data = request.get_json() #taking new values for inserting

    new_Fname = request_data['f_name']
    new_Lname = request_data['l_name']
    new_age = int(request_data['age'])
    new_room = int(request_data['room'])

    for record in rooms:
        if record['number'] == new_room:
            foreign_key = record['id']
    # for record in rooms:
    #     if record['number'] == new_room:
    #         print(count, record['capacity'])
    #         if count < record['capacity']:
    sql4 = (f"insert into resident(f_name, l_name, age, room) values"
            f"('{new_Fname}', '{new_Lname}', {new_age}, {foreign_key})")
    execute_myquery(con, sql4)
    return f"Resident {new_Fname} {new_Lname} successfully added."
    #         else:
    #             return "Error: Max capacity for this room reached"
    # return "none"
    
"""This block contains all the DELETE routes"""
@app.route("/api/resident", methods=['DELETE'])
def delete_resident():
    my_creds = creds.creds()
    con = create_con(my_creds.hostname, my_creds.username, my_creds.password, my_creds.database)
  
    f_name = request.args.get('f_name')  # get the id and status change from PUT request
    l_name = request.args.get('l_name')
    age = request.args.get('age')
    

    sql3 = f"delete from resident where f_name='{f_name}'and l_name ='{l_name}' and age = {age}"
    execute_myquery(con, sql3)
    return f'Resident {f_name} {l_name} successfully deleted.'


#route to delete floor
@app.route("/api/floor", methods=['DELETE'])
def delete_floor():
    
    my_creds = creds.creds()
    con = create_con(my_creds.hostname, my_creds.username, my_creds.password, my_creds.database)
     # taking new values for inserting
    new_level = request.args.get('level')
    
    sql2 = (f'delete from floor where level= {new_level}')
    execute_myquery(con, sql2)
    return f'Floor level:{new_level} successfully deleted.'

# #route to delete room
@app.route("/api/room", methods=['DELETE'])
def delete_room():

    my_creds = creds.creds()
    con = create_con(my_creds.hostname, my_creds.username, my_creds.password, my_creds.database)
    # taking new values for inserting
    target_number = request.args.get('number')

    sql3 = (f"delete from room where number={target_number}")
    execute_myquery(con, sql3)
    return f"Room number: {target_number} successfully deleted."


# # create a route that can update a room, floor, resident
"""This block contains all PUT routes"""
@app.route("/api/resident", methods=['PUT'])
def resident_update():
    
    my_creds = creds.creds()
    con = create_con(my_creds.hostname, my_creds.username, my_creds.password, my_creds.database)  
    sql = ("select resident.f_name, resident.l_name, resident.age, room.number as room from resident "
           "left join room on resident.room = room.id")
    residents = execute_read_myquery(con, sql)
    sql2 = "select * from room"
    rooms = execute_read_myquery(con, sql2)
    
    # get the id and status change from PUT request
    request_data = request.get_json()
    F_name = request_data['f_name']  
    L_name = request_data['l_name']
    age = int(request_data['age'])
    room_update = int(request_data['room'])
    
    for record in rooms:
        if record['number'] == room_update:
            foreign_key = record['id']
    avail_rooms =[]
    
    for record in rooms:
        avail_rooms.append(record['number'])

    if room_update in avail_rooms:
        sql3 = f"update resident set room='{foreign_key}' where f_name = '{F_name}' and l_name = '{L_name}' and age = {age}"
        execute_myquery(con, sql3)
        return f'Success: resident {F_name} {L_name} room number changed to {room_update}.'
    else:
        return "Error: new room number does exist"
    return "Error"

@app.route("/api/floor", methods=['PUT'])
def floor_update():
    # get the room number and status change from PUT request
    request_data = request.get_json()
    new_name = request_data['name'] 
    target_level = request_data['level']

    mycreds = creds.creds()
    con = create_con(mycreds.hostname, mycreds.username, mycreds.password, mycreds.database)
    sql = f"update floor set name='{new_name}' where level={target_level}"
    execute_myquery(con, sql)
    return f'Floor name successfully updated to {new_name}.'

@app.route("/api/room", methods=['PUT'])
def room_update():
    my_creds = creds.creds()
    con = create_con(my_creds.hostname, my_creds.username, my_creds.password, my_creds.database)  
    
    request_data = request.get_json() #taking new values for inserting
    new_capacity = request_data['capacity']
    target_number = request_data['number']
    target_floor = request_data['floor']
    
    sql3 = f"update room set capacity={new_capacity} where number={target_number}"
    execute_myquery(con, sql3)
    return f"Room capacity successfully updated to {new_capacity}."



app.run()