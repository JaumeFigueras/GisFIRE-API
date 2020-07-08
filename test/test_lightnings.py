import pytest
import testing.postgresql
from configparser import ConfigParser
from pathlib import Path
import psycopg2
import base64
import responses

from lightnings.meteocat import lightnings

def add_postgis(conn):
    cur = conn.cursor()
    cur.execute("CREATE EXTENSION postgis")
    cur.close()
    conn.commit()

def process_sql_file(filename, conn):
    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()
    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')
    # Execute every command from the input file
    c = conn.cursor()
    for command in sqlCommands:
        try:
            sc = command.strip()
            if len(sc) > 0:
                c.execute(sc)
        except Exception as e:
            print(command)
            print("Command skipped: " + str(e) + "\n")
    conn.commit()

@pytest.fixture
def client():
    test_folder = Path(__file__).parent

    lightnings.app.config['TESTING'] = True
    lightnings.app.config['CONFIG_FILE'] = str(test_folder) + '/gisfire_test.cfg'
    lightnings.app.config['CONFIG_OPTIONS'] = ConfigParser()
    lightnings.app.config['CONFIG_OPTIONS'].read(lightnings.app.config['CONFIG_FILE'])

    psql = testing.postgresql.Postgresql(host='127.0.0.1', port=9876, database='test', user='postgres')
    conn = psycopg2.connect(host='127.0.0.1', port=9876, database='test', user='postgres')
    cursor = conn.cursor()
    sql = "CREATE USER gisfireuser WITH PASSWORD '1234'"
    cursor.execute(sql)
    sql = "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO gisfireuser"
    cursor.execute(sql)
    conn.commit()
    add_postgis(conn)
    process_sql_file(str(test_folder.parent) + '/tokens/tokens.sql', conn)
    process_sql_file(str(test_folder.parent) + '/lightnings/meteocat/lightnings.sql', conn)
    conn.close()
    opt = lightnings.app.config['CONFIG_OPTIONS']['database']
    conn = psycopg2.connect(host=opt['host'], port=opt['port'], database=opt['database'], user=opt['user'], password=opt['password'])
    lightnings.app.config['TEST_CONNECTION'] = conn
    process_sql_file(str(test_folder) + '/database_init.sql', conn)

    with lightnings.app.test_client() as client:
        yield client

    psql.stop()

def test_database(client):
    """ Test that the database is correctly populated """
    conn = lightnings.app.config['TEST_CONNECTION']
    sql = "SELECT * FROM tokens"
    cursor = conn.cursor()
    cursor.execute(sql)
    assert cursor.rowcount == 4
    sql = "SELECT * FROM xdde_requests"
    cursor = conn.cursor()
    cursor.execute(sql)
    assert cursor.rowcount == 3
    sql = "SELECT * FROM lightnings"
    cursor = conn.cursor()
    cursor.execute(sql)
    assert cursor.rowcount == 3

def test_root_route(client):
    """ Test root route, empty json should be returned and one log entry added
    """
    # No Auth
    rv = client.get('/')
    conn = lightnings.app.config['TEST_CONNECTION']
    sql = "SELECT * FROM access"
    cursor = conn.cursor()
    cursor.execute(sql)
    assert not bool(rv.get_json())
    assert cursor.rowcount == 1
    sql = "DELETE FROM access"
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()

def test_root_route_user_undefined(client):
    """ Test root route, empty json should be returned and one log entry added.
    An unknown user authentication is passed, but as root route is just a
    'bonjour' service no error is thrown
    """
    # Auth of a not defined user
    username = 'test'
    password = 'test'
    rv = client.get('/', headers={'Authorization': 'Basic ' + base64.b64encode(bytes(username + ":" + password, 'ascii')).decode('ascii')})
    conn = lightnings.app.config['TEST_CONNECTION']
    sql = "SELECT * FROM access"
    cursor = conn.cursor()
    cursor.execute(sql)
    assert not bool(rv.get_json())
    assert cursor.rowcount == 1
    sql = "DELETE FROM access"
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()

def test_root_route_user_wrong_password(client):
    """ Test root route, empty json should be returned and one log entry added.
    An user with a wrong password authentication is passed, but as root route is
    just a 'bonjour' service no error is thrown
    """
    # Auth of wrong password
    username = 'user'
    password = 'test'
    rv = client.get('/', headers={'Authorization': 'Basic ' + base64.b64encode(bytes(username + ":" + password, 'ascii')).decode('ascii')})
    conn = lightnings.app.config['TEST_CONNECTION']
    sql = "SELECT * FROM access"
    cursor = conn.cursor()
    cursor.execute(sql)
    assert not bool(rv.get_json())
    assert cursor.rowcount == 1
    sql = "DELETE FROM access"
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()

def test_root_route_user_correct_password(client):
    """ Test root route, empty json should be returned and one log entry added.
    An user ans password authentication is passed, but as root route is just a
    'bonjour' service no error is thrown
    """
    # Auth with correct user and password
    username = 'user'
    password = 'user'
    rv = client.get('/', headers={'Authorization': 'Basic ' + base64.b64encode(bytes(username + ":" + password, 'ascii')).decode('ascii')})
    conn = lightnings.app.config['TEST_CONNECTION']
    sql = "SELECT * FROM access"
    cursor = conn.cursor()
    cursor.execute(sql)
    assert not bool(rv.get_json())
    assert cursor.rowcount == 1
    sql = "DELETE FROM access"
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()

def test_root_route_user_expired_wrong_password(client):
    """ Test root route, empty json should be returned and one log entry added.
    An expired with a wrong password authentication is passed, but as root route
    is just a 'bonjour' service no error is thrown
    """
    # Auth of an expired user with worng password
    username = 'user_old'
    password = 'test'
    rv = client.get('/', headers={'Authorization': 'Basic ' + base64.b64encode(bytes(username + ":" + password, 'ascii')).decode('ascii')})
    conn = lightnings.app.config['TEST_CONNECTION']
    sql = "SELECT * FROM access"
    cursor = conn.cursor()
    cursor.execute(sql)
    assert not bool(rv.get_json())
    assert cursor.rowcount == 1
    sql = "DELETE FROM access"
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()

def test_root_route_user_expired_correct_password(client):
    """ Test root route, empty json should be returned and one log entry added.
    An expired with password authentication is passed, but as root route is just
    a 'bonjour' service no error is thrown
    """
    # Auth of an expired user with password
    username = 'user_old'
    password = 'user'
    rv = client.get('/', headers={'Authorization': 'Basic ' + base64.b64encode(bytes(username + ":" + password, 'ascii')).decode('ascii')})
    conn = lightnings.app.config['TEST_CONNECTION']
    sql = "SELECT * FROM access"
    cursor = conn.cursor()
    cursor.execute(sql)
    assert not bool(rv.get_json())
    assert cursor.rowcount == 1
    sql = "DELETE FROM access"
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()

def test_root_route_cant_write_to_log(client):
    """ Test root route limiting database write, en error should be thrown
    """
    # No auth
    conn = lightnings.app.config['TEST_CONNECTION']
    sql = "REVOKE INSERT, UPDATE, DELETE ON access FROM gisfireuser;"
    cursor = conn.cursor()
    cursor.execute(sql)
    cursor.close()
    conn.commit()
    rv = client.get('/')
    assert rv.get_json()['status_code'] == 500
    sql = "GRANT INSERT, UPDATE, DELETE ON access TO gisfireuser;"
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()

def test_lightning_route_no_auth(client):
    """ Test lightning route, unauthorized error should be returned """
    # No Auth
    rv = client.get('/2020/6/1/10')
    assert rv.get_json()['status_code'] == 401

def test_lightning_route_wrong_user(client):
    """ Test lightning route, unauthorized error should be returned """
    # Wrong username
    username = 'wrong'
    password = 'wrong'
    rv = client.get('/2020/6/1/10', headers={'Authorization': 'Basic ' + base64.b64encode(bytes(username + ":" + password, 'ascii')).decode('ascii')})
    assert rv.get_json()['status_code'] == 401

def test_lightning_route_correct_user_wrong_password(client):
    """ Test lightning route, unauthorized error should be returned """
    # Wrong username
    username = 'user'
    password = 'wrong'
    rv = client.get('/2020/6/1/10', headers={'Authorization': 'Basic ' + base64.b64encode(bytes(username + ":" + password, 'ascii')).decode('ascii')})
    assert rv.get_json()['status_code'] == 401

def test_lightning_route_expired_user_correct_password(client):
    """ Test lightning route, unauthorized error should be returned """
    # Wrong username
    username = 'user_old'
    password = 'user'
    rv = client.get('/2020/6/1/10', headers={'Authorization': 'Basic ' + base64.b64encode(bytes(username + ":" + password, 'ascii')).decode('ascii')})
    assert rv.get_json()['status_code'] == 401
    assert rv.get_json()['message'] == 'user expired'

def test_lightning_route_wrong_year(client):
    """ Test wrong year in URL, an string is passed as year """
    # Wrong username
    username = 'user'
    password = 'user'
    rv = client.get('/hello/6/1/10', headers={'Authorization': 'Basic ' + base64.b64encode(bytes(username + ":" + password, 'ascii')).decode('ascii')})
    assert rv.get_json()['status_code'] == 400
    assert rv.get_json()['message'] == 'invalid paramaters'
    rv = client.get('/202/6/1/10', headers={'Authorization': 'Basic ' + base64.b64encode(bytes(username + ":" + password, 'ascii')).decode('ascii')})
    assert rv.get_json()['status_code'] == 400
    assert rv.get_json()['message'] == 'invalid year'
    rv = client.get('/20202/6/1/10', headers={'Authorization': 'Basic ' + base64.b64encode(bytes(username + ":" + password, 'ascii')).decode('ascii')})
    assert rv.get_json()['status_code'] == 400
    assert rv.get_json()['message'] == 'invalid year'

def test_lightning_route_wrong_month(client):
    """ Test wrong month in URL, an string is passed as month """
    # Wrong username
    username = 'user'
    password = 'user'
    rv = client.get('/2020/hello/1/10', headers={'Authorization': 'Basic ' + base64.b64encode(bytes(username + ":" + password, 'ascii')).decode('ascii')})
    assert rv.get_json()['status_code'] == 400
    assert rv.get_json()['message'] == 'invalid paramaters'
    rv = client.get('/2020/-3/1/10', headers={'Authorization': 'Basic ' + base64.b64encode(bytes(username + ":" + password, 'ascii')).decode('ascii')})
    assert rv.get_json()['status_code'] == 400
    assert rv.get_json()['message'] == 'invalid month'
    rv = client.get('/2020/33/1/10', headers={'Authorization': 'Basic ' + base64.b64encode(bytes(username + ":" + password, 'ascii')).decode('ascii')})
    assert rv.get_json()['status_code'] == 400
    assert rv.get_json()['message'] == 'invalid month'

def test_lightning_route_wrong_day(client):
    """ Test wrong day in URL, an string is passed as day """
    # Wrong username
    username = 'user'
    password = 'user'
    rv = client.get('/2020/06/hello/10', headers={'Authorization': 'Basic ' + base64.b64encode(bytes(username + ":" + password, 'ascii')).decode('ascii')})
    assert rv.get_json()['status_code'] == 400
    assert rv.get_json()['message'] == 'invalid paramaters'
    rv = client.get('/2020/06/-1/10', headers={'Authorization': 'Basic ' + base64.b64encode(bytes(username + ":" + password, 'ascii')).decode('ascii')})
    assert rv.get_json()['status_code'] == 400
    assert rv.get_json()['message'] == 'invalid day'
    rv = client.get('/2020/06/111/10', headers={'Authorization': 'Basic ' + base64.b64encode(bytes(username + ":" + password, 'ascii')).decode('ascii')})
    assert rv.get_json()['status_code'] == 400
    assert rv.get_json()['message'] == 'invalid day'

def test_lightning_route_wrong_hour(client):
    """Test wrong hour in URL, an string is passed as hour  """
    # Wrong username
    username = 'user'
    password = 'user'
    rv = client.get('/2020/06/01/hello', headers={'Authorization': 'Basic ' + base64.b64encode(bytes(username + ":" + password, 'ascii')).decode('ascii')})
    assert rv.get_json()['status_code'] == 400
    assert rv.get_json()['message'] == 'invalid paramaters'
    rv = client.get('/2020/06/01/-10', headers={'Authorization': 'Basic ' + base64.b64encode(bytes(username + ":" + password, 'ascii')).decode('ascii')})
    assert rv.get_json()['status_code'] == 400
    assert rv.get_json()['message'] == 'invalid hour'
    rv = client.get('/2020/06/01/33', headers={'Authorization': 'Basic ' + base64.b64encode(bytes(username + ":" + password, 'ascii')).decode('ascii')})
    assert rv.get_json()['status_code'] == 400
    assert rv.get_json()['message'] == 'invalid hour'

def test_lightning_route_wrong_date(client):
    """ Test a correctly formed date, but non existent in a real calendar """
    # Wrong username
    username = 'user'
    password = 'user'
    rv = client.get('/2020/02/30/10', headers={'Authorization': 'Basic ' + base64.b64encode(bytes(username + ":" + password, 'ascii')).decode('ascii')})
    assert rv.get_json()['status_code'] == 400
    assert rv.get_json()['message'] == 'invalid date'
    rv = client.get('/2045/06/01/10', headers={'Authorization': 'Basic ' + base64.b64encode(bytes(username + ":" + password, 'ascii')).decode('ascii')})
    assert rv.get_json()['status_code'] == 400
    assert rv.get_json()['message'] == 'invalid date'

def test_lightning_route_wrong_log(client):
    """ Test exception during write in the log table, it is tested revokingq user privileges """
    conn = lightnings.app.config['TEST_CONNECTION']
    sql = "REVOKE INSERT, UPDATE, DELETE ON access FROM gisfireuser;"
    cursor = conn.cursor()
    cursor.execute(sql)
    cursor.close()
    conn.commit()
    # Correct Auth
    username = 'user'
    password = 'user'
    rv = client.get('/2020/06/01/10', headers={'Authorization': 'Basic ' + base64.b64encode(bytes(username + ":" + password, 'ascii')).decode('ascii')})
    assert rv.get_json()['status_code'] == 500
    assert rv.get_json()['message'] == 'failed log action'
    sql = "GRANT INSERT, UPDATE, DELETE ON access TO gisfireuser;"
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()

def test_lightning_route_existing_with_0_lightnings(client):
    """ Test a previously cached query with success but with 0 lightnings """
    # Correct Auth
    username = 'user'
    password = 'user'
    rv = client.get('/2020/06/01/17', headers={'Authorization': 'Basic ' + base64.b64encode(bytes(username + ":" + password, 'ascii')).decode('ascii')})
    assert len(rv.get_json()) == 0
    conn = lightnings.app.config['TEST_CONNECTION']
    sql = "SELECT * FROM access"
    cursor = conn.cursor()
    cursor.execute(sql)
    assert cursor.rowcount == 1
    sql = "DELETE FROM access"
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()

def test_lightning_route_existing_with_3_lightnings(client):
    """ Test a previously cached query with success with some lightnings in the database """
    # Correct Auth
    username = 'user'
    password = 'user'
    rv = client.get('/2020/06/01/18', headers={'Authorization': 'Basic ' + base64.b64encode(bytes(username + ":" + password, 'ascii')).decode('ascii')})
    assert len(rv.get_json()) == 3
    conn = lightnings.app.config['TEST_CONNECTION']
    sql = "SELECT * FROM access"
    cursor = conn.cursor()
    cursor.execute(sql)
    assert cursor.rowcount == 1
    sql = "DELETE FROM access"
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    

def test_lightning_route_existing_error_with_0_lightnings(client):
    """ Test a previously cached query with error with no lightnings in remote """
    # TODO: add response
    # Correct Auth
    username = 'user'
    password = 'user'
    rv = client.get('/2020/06/01/19', headers={'Authorization': 'Basic ' + base64.b64encode(bytes(username + ":" + password, 'ascii')).decode('ascii')})
    assert len(rv.get_json()) == 0
    conn = lightnings.app.config['TEST_CONNECTION']
    sql = "SELECT * FROM xdde_requests WHERE result_code = 200"
    cursor = conn.cursor()
    cursor.execute(sql)
    assert cursor.rowcount == 3
    sql = "SELECT * FROM lightnings"
    cursor = conn.cursor()
    cursor.execute(sql)
    assert cursor.rowcount = 3
    sql = "UPDATE xdde_requests SET response_code = 500 WHERE year = 2020 AND month = 6 AND day = 1 AND hour = 19"
    cursor = conn.cursor()
    cursor.execute()
    conn.commit()
    
def test_lightning_route_existing_with_error_3_lightnings(client):
    """ Test a previously cached query with error with some lightnings in remote """
    # TODO
    # Correct Auth
    username = 'user'
    password = 'user'
    rv = client.get('/2020/06/01/18', headers={'Authorization': 'Basic ' + base64.b64encode(bytes(username + ":" + password, 'ascii')).decode('ascii')})
    assert len(rv.get_json()) == 3
    conn = lightnings.app.config['TEST_CONNECTION']
    sql = "SELECT * FROM access"
    cursor = conn.cursor()
    cursor.execute(sql)
    assert cursor.rowcount == 1
    sql = "DELETE FROM access"
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    
def test_lightning_route_new_with_0_lightnings(client):
    """ Test a new query with success with zero lightnings in the remote """
    # TODO
    # Correct Auth
    username = 'user'
    password = 'user'
    rv = client.get('/2020/06/01/18', headers={'Authorization': 'Basic ' + base64.b64encode(bytes(username + ":" + password, 'ascii')).decode('ascii')})
    assert len(rv.get_json()) == 3
    conn = lightnings.app.config['TEST_CONNECTION']
    sql = "SELECT * FROM access"
    cursor = conn.cursor()
    cursor.execute(sql)
    assert cursor.rowcount == 1
    sql = "DELETE FROM access"
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    
def test_lightning_route_new_with_3_lightnings(client):
    """ Test a new query with success with some lightnings in remote """
    # TODO
    # Correct Auth
    username = 'user'
    password = 'user'
    rv = client.get('/2020/06/01/18', headers={'Authorization': 'Basic ' + base64.b64encode(bytes(username + ":" + password, 'ascii')).decode('ascii')})
    assert len(rv.get_json()) == 3
    conn = lightnings.app.config['TEST_CONNECTION']
    sql = "SELECT * FROM access"
    cursor = conn.cursor()
    cursor.execute(sql)
    assert cursor.rowcount == 1
    sql = "DELETE FROM access"
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    
def test_lightning_route_new_with_error(client):
    """ Test a new query with success with remote error """
    # TODO
    # Correct Auth
    username = 'user'
    password = 'user'
    rv = client.get('/2020/06/01/18', headers={'Authorization': 'Basic ' + base64.b64encode(bytes(username + ":" + password, 'ascii')).decode('ascii')})
    assert len(rv.get_json()) == 3
    conn = lightnings.app.config['TEST_CONNECTION']
    sql = "SELECT * FROM access"
    cursor = conn.cursor()
    cursor.execute(sql)
    assert cursor.rowcount == 1
    sql = "DELETE FROM access"
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
