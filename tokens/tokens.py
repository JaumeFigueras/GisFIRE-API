from flask import Flask
from flask_httpauth import HTTPBasicAuth

import random
import psycopg2
import configparser

app = Flask(__name__)
auth = HTTPBasicAuth()

CONFIG = configparser.ConfigParser()
CONFIG.read('/home/gisfire/gisfire.cfg')
DB_CONNECTION = psycopg2.connect(host=CONFIG['database']['host'],
                                    port=CONFIG['database']['port'],
                                    database=CONFIG['database']['database'],
                                    user=CONFIG['database']['user'],
                                    password=CONFIG['database']['password'])
CHARACTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ:_!$€@"

def get_random_string(length):
    token = ""
    for i in range(length):
        token += CHARACTERS[random.randint(0, length-1)]
    return token

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@app.route('/', methods=['GET'])
@auth.login_required
def hello_world():
    return 'GisFIRE API:'

if __name__ == "__main__":
    app.run()
