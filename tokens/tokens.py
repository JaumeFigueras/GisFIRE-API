from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask import request
from flask import g
from flask import jsonify

import random
import psycopg2
import configparser
import datetime
import dateutil.parser

CHARACTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ:_!$€@"

app = Flask(__name__)
auth = HTTPBasicAuth()

def get_random_string(length):
    token = ""
    for i in range(length):
        token += CHARACTERS[random.randint(0, len(CHARACTERS) - 1)]
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

@app.errorhandler(401)
def page_not_found(error):
    return jsonify({'status_code': 401}), 401

@app.errorhandler(404)
def page_not_found(error):
    return jsonify({'status_code': 404}), 404

@auth.error_handler
def auth_error(status):
    return jsonify({'status_code': 401}), 401

@auth.verify_password
def verify_password(username, password):
    if username is None or username == '':
        return None
    sql ="SELECT token, admin, id, valid_until FROM tokens WHERE username = %s"
    cursor = g.DB_CONNECTION.cursor()
    cursor.execute(sql, (username, ))
    row = cursor.fetchone()
    if row is not None:
        if password == row[0]:
            user = {'username': username, 'password': password, 'admin': row[1], 'id': row[2], 'valid_until': row[3]}
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
    try:
        cursor = g.DB_CONNECTION.cursor()
        cursor.execute(sql)
        if cursor.rowcount != 1:
            cursor.close()
            g.DB_CONNECTION.rollback()
            return jsonify({'status_code': 500}), 500
        g.DB_CONNECTION.commit()
        cursor.close()
        return jsonify({})
    except:
        return jsonify({'status_code': 500}), 500

@app.route('/token', methods=['POST'])
@auth.login_required(role='admin')
def token():
    # If there aren't all the required paramaters a bad request is thrown
    if 'username' not in request.json or 'valid_until' not in request.json:
        return jsonify({'status_code': 400, 'message': 'username and valid_until parameters are expected'}), 400
    user = auth.current_user()
    inet = request.remote_addr
    username = request.json['username']
    # If valid_until format is not valid a bad request is thrown
    try:
        valid_until = dateutil.parser.parse(request.json['valid_until'])
    except:
        return jsonify({'status_code': 400, 'message': 'invalid valid_until date format'}), 400
    # If valid_until is not grater than today a bad request is thrown
    if datetime.datetime.utcnow() > valid_until:
        return jsonify({'status_code': 400, 'message': 'invalid valid_until date value'}), 400
    password = get_random_string(64)
    # Build queries
    sql_access = "INSERT INTO access (token_id, ip, url) VALUES ({0:}, '{1:}', '/token')".format(user['id'], inet)
    sql_tokens = "INSERT INTO tokens (username, token, admin, valid_until) VALUES (%s, '{0}', FALSE, '{1}')".format(password, valid_until.strftime("%Y-%m-%dT%H:%M:%SZ"))
    try:
        cursor = g.DB_CONNECTION.cursor()
        cursor.execute(sql_tokens)
        if cursor.rowcount != 1:
            cursor.close()
            g.DB_CONNECTION.rollback()
            return jsonify({'status_code': 500}), 500
        cursor.execute(sql_access)
        if cursor.rowcount != 1:
            cursor.close()
            g.DB_CONNECTION.rollback()
            return jsonify({'status_code': 500}), 500
        g.DB_CONNECTION.commit()
        cursor.close()
        return jsonify({'username': username, 'token': password})
    except:
        return jsonify({'status_code': 500}), 500

if __name__ == "__main__":
    app.run()

"""
out = open("/home/gisfire/out.txt","a")
out.write("valid_until:" + request.json['valid_until'] + "\n")
out.close()
"""
