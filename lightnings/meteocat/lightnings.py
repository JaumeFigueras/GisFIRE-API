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
import concurrent.futures
import requests

app = Flask(__name__)
auth = HTTPBasicAuth()

def download_thread(year, month, day, hour, api_key):
    """Download function of the meteo.cat dataof the selected date and hour. It
    uses tha API KEY provided bu the user to access the meteo.cat resources

    :param date: the date of the data to download
    :type date: datetime.date

    :param hour: the hour of the data to download
    :type hour: int

    :param api_key: the API KEY provided by meteo.cat to access its resources
    :type api_key: string

    :return: the success of the download operation and data received as json
    object extracted from the server response
    :type return: (bool, object)
    """
    base_url = "https://api.meteo.cat/xdde/v1"
    query = "/catalunya/{0:04d}/{1:02d}/{2:02d}/{3:02d}".format(year, month, day, hour)
    url = base_url + query
    headers = {"x-api-key": "{0:}".format(api_key)}
    r = requests.get(url, headers=headers)
    return (r.status_code, r.json())


@app.before_request
def config_setup():
    g.CONFIG = configparser.ConfigParser()
    g.CONFIG.read('/home/gisfire/gisfire.cfg')
    g.DB_CONNECTION = psycopg2.connect(host=g.CONFIG['lightnings']['host'],
                                        port=g.CONFIG['lightnings']['port'],
                                        database=g.CONFIG['lightnings']['database'],
                                        user=g.CONFIG['lightnings']['user'],
                                        password=g.CONFIG['lightnings']['password'])
    g.DB_GISFIRE = psycopg2.connect(host=g.CONFIG['database']['host'],
                                    port=g.CONFIG['database']['port'],
                                    database=g.CONFIG['database']['database'],
                                    user=g.CONFIG['database']['user'],
                                    password=g.CONFIG['database']['password'])

@app.teardown_appcontext
def close_db(error):
    g.DB_CONNECTION.close()
    g.DB_GISFIRE.close()

@app.errorhandler(401)
def unauthorized(error):
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
    cursor = g.DB_GISFIRE.cursor()
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
    sql = "INSERT INTO access (token_id, ip, url, method) VALUES ({0:}, '{1:}', '/lightnings/meteocat/v1/', 'GET')".format(user['id'] if user is not None else 'NULL', inet)
    try:
        cursor = g.DB_GISFIRE.cursor()
        cursor.execute(sql)
        if cursor.rowcount != 1:
            cursor.close()
            g.DB_GISFIRE.rollback()
            return jsonify({'status_code': 500}), 500
        g.DB_GISFIRE.commit()
        cursor.close()
        return jsonify({})
    except:
        return jsonify({'status_code': 500}), 500

@app.route('/<year>/<month>/<day>/<hour>', methods=['GET'])
@auth.login_required()
def retrieve_lightnings(year, month, day, hour):
    # Get basic data
    user = auth.current_user()
    inet = request.remote_addr
    # Try to convert all parameters to integers
    try:
        year = int(year)
        month = int(month)
        day = int(day)
        hour = int(hour)
    except:
        return jsonify({'status_code': 400, 'message': 'invalid paramaters'}), 400
    # If all the parameters are correct, is a possible date?
    if year < 1900 or year > 9999:
        return jsonify({'status_code': 400, 'message': 'invalid year'}), 400
    if month < 0 or month > 12:
        return jsonify({'status_code': 400, 'message': 'invalid month'}), 400
    if day < 0 or day > 31:
        return jsonify({'status_code': 400, 'message': 'invalid day'}), 400
    if hour < 0 or hour > 23:
        return jsonify({'status_code': 400, 'message': 'invalid hour'}), 400
    # It seems a date but is the 31 of february?
    try:
        date = datetime.datetime(year=year, month=month, day=day, hour=hour)
        if date > datetime.datetime.utcnow():
            return jsonify({'status_code': 400, 'message': 'invalid date'}), 400
    except:
        return jsonify({'status_code': 400, 'message': 'invalid date'}), 400
    # The date is valid, let's log the access
    sql_access = "INSERT INTO access (token_id, ip, url, method) VALUES ({0:}, '{1:}', '/lightnings/meteocat/v1/{3:}/{4:}/{5:}/{6:}', '{2:}')".format(user['id'], inet, request.method, year, month, day, hour)
    try:
        cursor = g.DB_GISFIRE.cursor()
        cursor.execute(sql_access)
        if cursor.rowcount != 1:
            cursor.close()
            g.DB_GISFIRE.rollback()
            return jsonify({'status_code': 500, 'message': 'failed log action'}), 500
        g.DB_GISFIRE.commit()
        cursor.close()
    except:
        return jsonify({'status_code': 500, 'message': 'failed log action'}), 500
    # Now check if this request is neo or not
    sql_lightnings = "SELECT result_code, number_of_lightnings FROM xdde_requests \
                        WHERE year = {0:} AND month = {1:} AND day = {2:} AND hour = {3:}"
                        .format(year, month, day, hour)
    try:
        cursor = g.DB_CONNECTION.cursor()
        cursor.execute(sql_lightnings)
        if cursor.rowcount > 1:
            return jsonify({'status_code': 500, 'message': 'database inconsistency on xdde_requests'}), 500
        elif cursor.rowcount == 1:
            rows = cursor.fetchall()
            new_request = False
            old_request_status_code = rows[0][0]
        else:
            new_request = True
        cursor.close()
    except:
        return jsonify({'status_code': 500, 'message': 'failed request check'}), 500
    # Launch request to MeteoCat
    if new_request or (not new_request and old_request_status_code != 200):
        meteocat_api_key = request.headers.get('x-api-key')
        return_code, lightnings = download_thread(year, month, day, hour, meteocat_api_key)
        if return_code == 200:
            if new_request:
                sql_lightnings = "INSERT INTO xdde_requests (year, month, day, hour, result_code, number_of_lightnings)\
                                    VALUES ({0:}, {1:}, {2:}, {3:}, {4:}, {5:}, )".format(year, month, day, hour, return_code, len(lightnings))
            else:
                sql_lightnings = "UPDATE xdde_requests SET result_code = {0:}, number_of_lightnings = {1:}".format(return_code, len(lightnings))
        else:
            sql_lightnings = "INSERT INTO xdde_requests (year, month, day, hour, result_code)\
                                VALUES ({0:}, {1:}, {2:}, {3:}, {4:})".format(year, month, day, hour, return_code)
        try:
            cursor = g.DB_CONNECTION.cursor()
            cursor.execute(sql_lightnings)
            if cursor.rowcount =! 1:
                g.DB_CONNECTION.rollback()
                cursor.close()
                return jsonify({'status_code': 500, 'message': 'database error on xdde_requests'}), 500
            g.DB_CONNECTION.commit()
            cursor.close()
            if return_code != 200:
                return jsonify({'status_code': 502, 'message': 'error while accessing remote server'}), 502
        except:
            return jsonify({'status_code': 500, 'message': 'database error on xdde_requests'}), 500
        # At this point the database has to be populated with lightnings
        sql_lightnings = list()
        for ln in lightnings:
            sql_lightnings.append("INSERT INTO lightnings (_id, _data, _correntPic, _chi2, _ellipse_eixMajor, _ellipse_eixMenor, _ellipse_angle, _numSensors, _nuvolTerra, _idMunicipi, _coordenades_latitud, _coordenades_longitud) \
                                    VALUES ({0:}, {1:}, {2:}, {3:}, {4:}, {5:}, {6:}, {7:}, {8:}, {9:}, {10:}, )").format(
                                    ln['id'], ln['data'], ln['correntPic'], ln['chi2'], ln['ellipse']['eixMajor'], ln['ellipse']['eixMenor'], ln['ellipse']['angle'], ln['numSensors'], ln['nuvolTerra'], ln['idMunicipi'] if 'idMunicipi' in ln else 'NULL', ln['coordenades']['longitud'], ln['coordenades']['latitud'])
                                    )
        try:
            cursor = g.DB_CONNECTION.cursor()
            cursor.execute(sql_lightnings)
            if cursor.rowcount =! len(sql_lightnings):
                g.DB_CONNECTION.rollback()
                cursor.close()
                return jsonify({'status_code': 500, 'message': 'database error on lightnings'}), 500
            g.DB_CONNECTION.commit()
            cursor.close()
        except:
            return jsonify({'status_code': 500, 'message': 'database error on lightnings'}), 500
    # Read the database and prepare json
    sql_lightnings = "SELECT _id, _data, _correntPic, _chi2, _ellipse_eixMajor, _ellipse_eixMenor, _ellipse_angle, _numSensors, _nuvolTerra, _idMunicipi, _coordenades_latitud, _coordenades_longitud FROM lightnings WHERE _data >= '{0:}:{1:}:{2:} {3:}-00-00'::timestamp AND _data <= '{0:}:{1:}:{2:} {3:}-59-59'::timestamp"
    cursor = g.DB_CONNECTION.cursor()
    cursor.execute(sql_lightnings)
    rows = cursor.fetchall()
    lightnings = list()
    for row in rows:
        ln = dict()
        ln['id'] = row[0]
        ln['data'] = row[1]
        ln['correntPic'] = row[2]
        ln['chi2'] = row[3]
        ln['ellipse'] = dict()
        ln['ellipse']['eixMajor'] = row[4]
        ln['ellipse']['eixMenor'] = row[5]
        ln['ellipse']['angle'] = row[6]
        ln['numSnesors'] = row[7]
        ln['nuvolTerra'] = row[8]
        ln['idMunicipi'] = row[9]
        ln['coordenades'] = dict()
        ln['coordenades']['longitud'] = row[10]
        ln['coordenades']['latitud'] = row[11]
        lightnings.append(ln)
    # Return data
    return jsonify(lighnings)


if __name__ == "__main__":
    app.run()

"""
out = open("/home/gisfire/out.txt","a")
out.write("valid_until:" + request.json['valid_until'] + "\n")
out.close()
"""
