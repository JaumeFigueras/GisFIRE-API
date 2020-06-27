from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask import request
from flask import g
from flask import jsonify

import random
import psycopg2
import configparser
import datetime

CHARACTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ:_!$€@"

app = Flask(__name__)
auth = HTTPBasicAuth()

def get_random_string(length):
    token = ""
    for i in range(length):
        token += CHARACTERS[random.randint(0, length-1)]
    return token

@app.before_request
def config_setup():
    g.CONFIG = configparser.ConfigParser()
    g.CONFIG.read('/home/gisfire/gisfire.cfg')
    g.DB_CONNECTION = psycopg2.connect(host=g.CONFIG['database']['host'],
                                        port=g.CONFIG['database']['port'],
                                        database=g.CONFIG['database']['database'],
                                        user=g.CONFIG['database']['user'],
                                        password=g.CONFIG['database']['password'])

@app.teardown_appcontext
def close_db(error):
    g.DB_CONNECTION.close()

@auth.verify_password
def verify_password(username, password):
    if username is None or username == '':
        return None
    sql ="SELECT token, admin, id FROM tokens WHERE username = %s"
    cursor = g.DB_CONNECTION.cursor()
    cursor.execute(sql, username)
    row = cursor.fetchone()
    if row is not None:
        if password == row[0]:
            user = {'username': username, 'password': password, 'admin': row[1], 'id': row[2]}
        else:
            user = None
    cursor.close()
    return user

@auth.get_user_roles
def get_user_roles(user):
    if user['admin'] == True:
        return ['admin']
    return ['user']

@app.route('/', methods=['GET'])
@auth.login_required(optional=True)
def hello_world():
    user = auth.current_user()
    inet = request.remote_addr
    sql = "INSERT INTO access (token_id, ip, url) VALUES ({0:}, '{1:}', '/')".format(user['id'] if user is not None else 'NULL', inet)
    cursor = g.DB_CONNECTION.cursor()
    cursor.execute(sql)
    g.DB_CONNECTION.commit()
    cursor.close()
    return jsonify({})

@app.route('/token', methods=['POST'])
@auth.login_required(role='admin')
def token():
    #TODO: Check dates and values
    #TODO: pass
    inet = request.remote_addr
    username = request.json['username']
    if 'valid_until' in request.json:
        valid_until = datettime.datetime(request.json['valid_until'])
    else:
        valid_until = None
    password = get_random_string(64)
    sql = sql = "INSERT INTO access (token_id, ip, url) VALUES ({0:}, '{1:}', '/token')".format(user['id'], inet)
    cursor = g.DB_CONNECTION.cursor()
    cursor.execute(sql)
    g.DB_CONNECTION.commit()
    if valid_until is not None:
        sql = sql = "INSERT INTO tokens (username, token, admin, valid_until) VALUES (%s, '{0}', FALSE, {1})".format(password, valid_until.strftime("%Y-%m-%dT%H:%M:%SZ"))
        cursor = g.DB_CONNECTION.cursor()
        cursor.execute(sql, (username))
    else:
        pass
    g.DB_CONNECTION.commit()
    return jsonify({'token': password})

if __name__ == "__main__":
    app.run()
