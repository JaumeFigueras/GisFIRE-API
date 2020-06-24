from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask import request

import random
import psycopg2
import configparser
import datetime

app = Flask(__name__)
auth = HTTPBasicAuth()

CONFIG = configparser.ConfigParser()
CONFIG.read('/home/gisfire/gisfire.cfg')
CHARACTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ:_!$€@"
DB_CONNECTION = None

def restore_db_connection():
    global DB_CONNECTION
    DB_CONNECTION = psycopg2.connect(host=CONFIG['database']['host'],
                                        port=CONFIG['database']['port'],
                                        database=CONFIG['database']['database'],
                                        user=CONFIG['database']['user'],
                                        password=CONFIG['database']['password'])
restore_db_connection()

def get_random_string(length):
    token = ""
    for i in range(length):
        token += CHARACTERS[random.randint(0, length-1)]
    return token

@auth.verify_password
def verify_password(username, password):
    sql ="SELECT token, admin, id FROM tokens WHERE username = '{0:}'".format(username)
    if DB_CONNECTION.closed:
        restore_db_connection()
    cursor = DB_CONNECTION.cursor()
    cursor.execute(sql)
    row = cursor.fetchone()
    if row is not None:
        if password == row[0]:
            return {'username': username, 'password': password, 'admin': row[1], 'id': row[2]}
    return None

@auth.get_user_roles
def get_user_roles(user):
    if user['admin'] == True:
        return ['admin']
    return ['user']

@app.route('/', methods=['GET'])
@auth.login_required(optional=True)
def hello_world():
    #TODO: Add url in sql
    #TODO: jsonify
    user = auth.current_user()
    inet = request.remote_addr
    if user is not None:
        sql = "INSERT INTO access (token_id, ip) VALUES ({0:}, '{1:}')".format(user['id'], inet)
    else:
        sql = "INSERT INTO access (token_id, ip) VALUES (NULL, '{0:}')".format(inet)
    if DB_CONNECTION.closed:
        restore_db_connection()
    cursor = DB_CONNECTION.cursor()
    cursor.execute(sql)
    DB_CONNECTION.commit()
    cursor.close()
    return 'GisFIRE API: tokens'

@app.route('/token', methods=['POST'])
@auth.login_required(role='admin')
def token():
    #TODO: Add url in sql
    #TODO: Check dates and values
    #TODO: pass
    #TODO: jsonify
    inet = request.remote_addr
    username = request.json['username']
    if 'valid_until' in request.json:
        valid_until = datettime.datetime(request.json['valid_until'])
    else:
        valid_until = None
    password = get_random_string(64)
    sql = sql = "INSERT INTO access (token_id, ip) VALUES ({0:}, '{1:}')".format(user['id'], inet)
    if DB_CONNECTION.closed:
        restore_db_connection()
    cursor = DB_CONNECTION.cursor()
    cursor.execute(sql)
    DB_CONNECTION.commit()
    if valid_until is not None:
        sql = sql = "INSERT INTO tokens (username, token, admin, valid_until) VALUES (%s, '{0}', FALSE, {1})".format(password, valid_until.strftime("%Y-%m-%dT%H:%M:%SZ"))
        if DB_CONNECTION.closed:
            restore_db_connection()
        cursor = DB_CONNECTION.cursor()
        cursor.execute(sql, (username))
    else:
        pass
    DB_CONNECTION.commit()
    return 'GisFIRE API:'

@app.teardown_appcontext
def close_db(error):
    if not DB_CONNECTION.closed:
        DB_CONNECTION.close()

if __name__ == "__main__":
    app.run()
