from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask import request

import random
import psycopg2
import configparser

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

def get_random_string(length):
    token = ""
    for i in range(length):
        token += CHARACTERS[random.randint(0, length-1)]
    return token

@auth.verify_password
def verify_password(username, password):
    sql ="SELECT token, admin, import ipdb; ipdb.set_trace() FROM tokens WHERE username = '{0:}'".format(username)
    if DB_CONNECTION is None:
        restore_db_connection()
    cursor = DB_CONNECTION.cursor()
    cursor.execute(sql)
    row = cursor.fetchone()
    if password == row[0]:
        return {'username': username, 'password': password, 'admin': row[1], 'role': 'admin', 'id': row[2]}
    return None

@app.route('/', methods=['GET'])
@auth.login_required(optional=True)
def hello_world():
    user = auth.current_user()
    inet = request.remote_addr
    if user is not None:
        sql = "INSERT INTO access (token_id, ip) VALUES ({0:}, '{1:}')".format(user['id'], inet)
    else:
        sql = "INSERT INTO access (token_id, ip) VALUES (NULL, '{0:}')".format(inet)
    if DB_CONNECTION is None:
        restore_db_connection()
    cursor = DB_CONNECTION.cursor()
    cursor.execute(sql)
    DB_CONNECTION.commit()
    cursor.close()
    return 'GisFIRE API: tokens'

@app.route('/token', methods=['POST'])
@auth.login_required
def token():
    return 'GisFIRE API:'

@app.teardown_appcontext
def close_db(error):
    if DB_CONNECTION is not None:
        DB_CONNECTION.close()


if __name__ == "__main__":
    app.run()
