import flask
from flask import request, make_response
from flask import jsonify

import hashlib
import datetime
import time

'''Taken from class API se'''


app = flask.Flask(__name__)
app.config['DEBUG'] = True

master_username = 'Kevin'
master_password = '0cc82c491a35894d1444e702d97e043f7a5911ec4ea4035414af27ee01c17c56'

#Basic authentication which uses username and password of request
@app.route('/auth', methods=['GET'])
def process_request():
    if request.authorization:
        encodedpasswd = request.authorization.password.encode() #gettign password in unicode values
        hashvalue = hashlib.sha256(encodedpasswd)
        if request.authorization.username == master_username and hashvalue.hexdigest() == master_password:
            return '<h1> Authenticated User </h1>'
    return make_response('Could not find user', 401, {'WWW-Authenticate:': 'Basic realm="Login Required"'})

# token to approve the credentials 
valid_tokens = {
    "100", "301", "5333"
}
@app.route('/api/token/<tokenno>', methods=['GET'])
def processtoken(tokenno):
    for eachtoken in valid_tokens:
        if eachtoken == tokenno:
            return '<h1> Authorized User </h1>'
    return '<h1> Unauthorized User </h1>'

# time tokens to approve the authentication of users credentials w.r.t time



# dateInSeconds = date.timestamp() 
# date = datetime.datetime(2022, 1, 1)

# @app.route('api/timetoken/<tokenno>', methods = ['GET'])
# def processtimetoken(tokenno):
#     if float(tokenno) > time.time():
#         return '<h1> Authenticated User </h1>'
#     return '<h1> Time token expired </h1>'

app.run()