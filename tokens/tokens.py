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
    return username

@app.route('/', methods=['GET'])
def hello_world():
    inet = request.remote_addr
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
