#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from base64 import b64encode
import json


def test_empty_api_meteocat_stations_entrypoint_01(api, postgresql_schema):
    """
    Tests the auth entry point without action.

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    response = api.get('/v1/meteocat/station/')
    assert response.content_type == 'application/json'
    assert response.status_code == 500
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 1
    assert data['status_code'] == 500
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 1
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    record = cursor.fetchone()
    assert record[1] is None
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/meteocat/station/'
    assert record[4] == 'GET'
    assert record[5] == '{}'
    assert record[6] == 500


def test_empty_api_meteocat_stations_entrypoint_02(api, postgresql_schema):
    """
    Tests the auth entry point without action.

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    response = api.get('/v1/meteocat/station')
    assert response.content_type == 'application/json'
    assert response.status_code == 500
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 1
    assert data['status_code'] == 500
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 1
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    record = cursor.fetchone()
    assert record[1] is None
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/meteocat/station'
    assert record[4] == 'GET'
    assert record[5] == '{}'
    assert record[6] == 500


def test_empty_api_meteocat_stations_nearest_parameters_01(api, postgresql_schema):
    """
    Tests the nearest station without parameters.

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8"))}
    response = api.get('/v1/meteocat/station/nearest/', headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 422
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 1
    assert data['status_code'] == 422
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 1
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    record = cursor.fetchone()
    assert record[1] == 3
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/meteocat/station/nearest/'
    assert record[4] == 'GET'
    assert record[5] == '{}'
    assert record[6] == 422


def test_empty_api_meteocat_stations_nearest_parameters_02(api, postgresql_schema):
    """
    Tests the nearest station with 5 parameters.

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8"))}
    response = api.get('/v1/meteocat/station/nearest?a=1&b=2&c=3&d=4&e=5', headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 422
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 1
    assert data['status_code'] == 422
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 1
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    record = cursor.fetchone()
    assert record[1] == 3
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/meteocat/station/nearest?a=1&b=2&c=3&d=4&e=5'
    assert record[4] == 'GET'
    assert json.loads(record[5]) == {"a": "1", "b": "2", "c": "3", "e": "5", "d": "4"}
    assert record[6] == 422


def test_empty_api_meteocat_stations_nearest_parameters_03(api, postgresql_schema):
    """
    Tests the nearest station with 3 parameters.

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8"))}
    response = api.get('/v1/meteocat/station/nearest?a=1&b=2&c=3', headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 422
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 1
    assert data['status_code'] == 422
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 1
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    record = cursor.fetchone()
    assert record[1] == 3
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/meteocat/station/nearest?a=1&b=2&c=3'
    assert record[4] == 'GET'
    assert json.loads(record[5]) == {"a": "1", "b": "2", "c": "3"}
    assert record[6] == 422


def test_empty_api_meteocat_stations_nearest_parameters_04(api, postgresql_schema):
    """
    Tests the nearest station with 4 parameters.

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8"))}
    response = api.get('/v1/meteocat/station/nearest?a=1&b=2&c=3&d=4', headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 422
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 1
    assert data['status_code'] == 422
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 1
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    record = cursor.fetchone()
    assert record[1] == 3
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/meteocat/station/nearest?a=1&b=2&c=3&d=4'
    assert record[4] == 'GET'
    assert json.loads(record[5]) == {"a": "1", "b": "2", "c": "3", "d": "4"}
    assert record[6] == 422


def test_empty_api_meteocat_stations_nearest_parameters_05(api, postgresql_schema):
    """
    Tests the nearest station with 4 parameters with date and SRID and no lat/lon or x/y.

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8"))}
    response = api.get('/v1/meteocat/station/nearest?date=2021-11-01T22:00:00Z&srid=4258&c=3&d=4', headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 422
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 1
    assert data['status_code'] == 422
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 1
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    record = cursor.fetchone()
    assert record[1] == 3
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/meteocat/station/nearest?date=2021-11-01T22:00:00Z&srid=4258&c=3&d=4'
    assert record[4] == 'GET'
    assert json.loads(record[5]) == {"date": "2021-11-01T22:00:00Z", "srid": "4258", "c": "3", "d": "4"}
    assert record[6] == 422


def test_empty_api_meteocat_stations_nearest_parameters_06(api, postgresql_schema):
    """
    Tests the nearest station with 4 parameters with date and SRID with wrong lat/lon.

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8"))}
    response = api.get('/v1/meteocat/station/nearest?date=2021-11-01T22:00:00Z&srid=4258&x=3.25&lat=4.58',
                       headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 422
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 1
    assert data['status_code'] == 422
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 1
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    record = cursor.fetchone()
    assert record[1] == 3
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/meteocat/station/nearest?date=2021-11-01T22:00:00Z&srid=4258&x=3.25&' \
                        'lat=4.58'
    assert record[4] == 'GET'
    assert json.loads(record[5]) == {"date": "2021-11-01T22:00:00Z", "srid": "4258", "lat": "4.58", "x": "3.25"}
    assert record[6] == 422


def test_empty_api_meteocat_stations_nearest_parameters_07(api, postgresql_schema):
    """
    Tests the nearest station with 4 parameters with date and SRID with wrong lat/lon.

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8"))}
    response = api.get('/v1/meteocat/station/nearest?date=2021-11-01T22:00:00Z&srid=4258&x=3.25&lon=4.58',
                       headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 422
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 1
    assert data['status_code'] == 422
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 1
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    record = cursor.fetchone()
    assert record[1] == 3
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/meteocat/station/nearest?date=2021-11-01T22:00:00Z&srid=4258&x=3.25&' \
                        'lon=4.58'
    assert record[4] == 'GET'
    assert json.loads(record[5]) == {"date": "2021-11-01T22:00:00Z", "srid": "4258", "lon": "4.58", "x": "3.25"}
    assert record[6] == 422


def test_empty_api_meteocat_stations_nearest_parameters_08(api, postgresql_schema):
    """
    Tests the nearest station with 4 parameters with incorrect date.

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8"))}
    response = api.get('/v1/meteocat/station/nearest?date=2021-13-01T22:05:37Z&srid=4258&lon=2.33371&lat=41.71408',
                       headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 400
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 1
    assert data['status_code'] == 400
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 1
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    record = cursor.fetchone()
    assert record[1] == 3
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/meteocat/station/nearest?date=2021-13-01T22:05:37Z&srid=4258&' \
                        'lon=2.33371&lat=41.71408'
    assert record[4] == 'GET'
    assert json.loads(record[5]) == {"date": "2021-13-01T22:05:37Z", "srid": "4258", "lon": "2.33371",
                                     "lat": "41.71408"}
    assert record[6] == 400


def test_empty_api_meteocat_stations_nearest_parameters_09(api, postgresql_schema):
    """
    Tests the nearest station with 4 parameters with incorrect srid.

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8"))}
    response = api.get('/v1/meteocat/station/nearest?date=2021-11-01T22:05:37Z&srid=4258a&lon=2.33371&lat=41.71408',
                       headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 400
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 1
    assert data['status_code'] == 400
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 1
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    record = cursor.fetchone()
    assert record[1] == 3
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/meteocat/station/nearest?date=2021-11-01T22:05:37Z&srid=4258a&' \
                        'lon=2.33371&lat=41.71408'
    assert record[4] == 'GET'
    assert json.loads(record[5]) == {"date": "2021-11-01T22:05:37Z", "srid": "4258a", "lon": "2.33371",
                                     "lat": "41.71408"}
    assert record[6] == 400


def test_empty_api_meteocat_stations_nearest_parameters_10(api, postgresql_schema):
    """
    Tests the nearest station with 4 parameters with incorrect lat.

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8"))}
    response = api.get('/v1/meteocat/station/nearest?date=2021-11-01T22:05:37Z&srid=4258&lon=2.33371&lat=41a.71408',
                       headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 400
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 1
    assert data['status_code'] == 400
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 1
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    record = cursor.fetchone()
    assert record[1] == 3
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/meteocat/station/nearest?date=2021-11-01T22:05:37Z&srid=4258&' \
                        'lon=2.33371&lat=41a.71408'
    assert record[4] == 'GET'
    assert json.loads(record[5]) == {"date": "2021-11-01T22:05:37Z", "srid": "4258", "lon": "2.33371",
                                     "lat": "41a.71408"}
    assert record[6] == 400


def test_empty_api_meteocat_stations_nearest_parameters_11(api, postgresql_schema):
    """
    Tests the nearest station with 4 parameters with incorrect lat.

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8"))}
    response = api.get('/v1/meteocat/station/nearest?date=2021-11-01T22:05:37Z&srid=4258&lon=2b.33371&lat=41.71408',
                       headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 400
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 1
    assert data['status_code'] == 400
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 1
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    record = cursor.fetchone()
    assert record[1] == 3
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/meteocat/station/nearest?date=2021-11-01T22:05:37Z&srid=4258&' \
                        'lon=2b.33371&lat=41.71408'
    assert record[4] == 'GET'
    assert json.loads(record[5]) == {"date": "2021-11-01T22:05:37Z", "srid": "4258", "lon": "2b.33371",
                                     "lat": "41.71408"}
    assert record[6] == 400


def test_empty_api_meteocat_stations_nearest_01(api, postgresql_schema):
    """
    Tests the nearest station with 4 parameters with incorrect lat.

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8"))}
    response = api.get('/v1/meteocat/station/nearest?date=2018-07-16T06:54:00Z&srid=4258&lon=1.87485&lat=42.23414',
                       headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    data = json.loads(response.get_data(as_text=True))
    print(data)
    assert len(data) == 17
    assert data['code'] == 'DG'
    assert data['altitude'] == 1971.4
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 1
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    record = cursor.fetchone()
    assert record[1] == 3
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/meteocat/station/nearest?date=2018-07-16T06:54:00Z&srid=4258&' \
                        'lon=1.87485&lat=42.23414'
    assert record[4] == 'GET'
    assert json.loads(record[5]) == {"date": "2018-07-16T06:54:00Z", "srid": "4258", "lon": "1.87485",
                                     "lat": "42.23414"}
    assert record[6] == 200

