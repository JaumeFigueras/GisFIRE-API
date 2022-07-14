#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from base64 import b64encode
from freezegun import freeze_time
from gisfire_meteocat_lib.remote_api import meteocat_urls
from gisfire_meteocat_lib.remote_api import meteocat_api
import requests
import json


def test_api_meteocat_data_entrypoint_01(api, postgresql_schema):
    """
    Tests the data entry point without action.

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    response = api.get('/v1/meteocat/data/')
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
    assert record[3] == 'http://localhost/v1/meteocat/data/'
    assert record[4] == 'GET'
    assert record[5] == '{}'
    assert record[6] == 500


def test_api_meteocat_data_entrypoint_02(api, postgresql_schema):
    """
    Tests the data entry point without action.

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    response = api.get('/v1/meteocat/data')
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
    assert record[3] == 'http://localhost/v1/meteocat/data'
    assert record[4] == 'GET'
    assert record[5] == '{}'
    assert record[6] == 500


def test_api_meteocat_data_measure_parameters_01(api, postgresql_schema):
    """
    Tests the data measure without parameters.

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8"))}
    response = api.get('/v1/meteocat/data/measure', headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 404
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 1
    assert data['status_code'] == 404
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 1
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    record = cursor.fetchone()
    assert record[1] is None
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/meteocat/data/measure'
    assert record[4] == 'GET'
    assert record[5] == '{}'
    assert record[6] == 404


def test_api_meteocat_data_measure_parameters_02(api, postgresql_schema):
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
    response = api.get('/v1/meteocat/data/measure/', headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 404
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 1
    assert data['status_code'] == 404
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 1
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    record = cursor.fetchone()
    assert record[1] is None
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/meteocat/data/measure/'
    assert record[4] == 'GET'
    assert record[5] == '{}'
    assert record[6] == 404


def test_api_meteocat_data_measure_parameters_03(api, postgresql_schema):
    """
    Tests the nearest station with wrong url.

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8"))}
    response = api.get('/v1/meteocat/data/measure/AA', headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 404
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 1
    assert data['status_code'] == 404
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 1
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    record = cursor.fetchone()
    assert record[1] is None
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/meteocat/data/measure/AA'
    assert record[4] == 'GET'
    assert record[5] == '{}'
    assert record[6] == 404


def test_api_meteocat_data_measure_parameters_04(api, postgresql_schema):
    """
    Tests the nearest station with wrong url.

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8"))}
    response = api.get('/v1/meteocat/data/measure/AA/', headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 404
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 1
    assert data['status_code'] == 404
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 1
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    record = cursor.fetchone()
    assert record[1] is None
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/meteocat/data/measure/AA/'
    assert record[4] == 'GET'
    assert record[5] == '{}'
    assert record[6] == 404


def test_api_meteocat_data_measure_parameters_05(api, postgresql_schema):
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
    response = api.get('/v1/meteocat/data/measure/AA/T', headers=headers)
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
    assert record[3] == 'http://localhost/v1/meteocat/data/measure/AA/T'
    assert record[4] == 'GET'
    assert record[5] == '{}'
    assert record[6] == 422


def test_api_meteocat_data_measure_parameters_06(api, postgresql_schema):
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
    response = api.get('/v1/meteocat/data/measure/AA/T/', headers=headers)
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
    assert record[3] == 'http://localhost/v1/meteocat/data/measure/AA/T/'
    assert record[4] == 'GET'
    assert record[5] == '{}'
    assert record[6] == 422


def test_api_meteocat_data_measure_parameters_07(api, postgresql_schema):
    """
    Tests the nearest station without date parameter.

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8"))}
    response = api.get('/v1/meteocat/data/measure/AA/T?a=1', headers=headers)
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
    assert record[3] == 'http://localhost/v1/meteocat/data/measure/AA/T?a=1'
    assert record[4] == 'GET'
    assert json.loads(record[5]) == {"a": "1"}
    assert record[6] == 422


def test_api_meteocat_data_measure_parameters_08(api, postgresql_schema):
    """
    Tests the nearest station with date parameter but with a total of 3 parameters.

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8"))}
    response = api.get('/v1/meteocat/data/measure/AA/T?date=2018-07-14T05:23:45Z&b=2&c=3', headers=headers)
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
    assert record[3] == 'http://localhost/v1/meteocat/data/measure/AA/T?date=2018-07-14T05:23:45Z&b=2&c=3'
    assert record[4] == 'GET'
    assert json.loads(record[5]) == {"date": "2018-07-14T05:23:45Z", "b": "2", "c": "3"}
    assert record[6] == 422


def test_api_meteocat_data_measure_parameters_09(api, postgresql_schema):
    """
    Tests the nearest station with incorrect date parameter.

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8"))}
    response = api.get('/v1/meteocat/data/measure/AA/T?date=2018-07-14T25:23:45Z', headers=headers)
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
    assert record[3] == 'http://localhost/v1/meteocat/data/measure/AA/T?date=2018-07-14T25:23:45Z'
    assert record[4] == 'GET'
    assert json.loads(record[5]) == {"date": "2018-07-14T25:23:45Z"}
    assert record[6] == 400


def test_api_meteocat_data_measure_parameters_10(api, postgresql_schema):
    """
    Tests the nearest station with incorrect operation parameter.

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8"))}
    response = api.get('/v1/meteocat/data/measure/AA/T?date=2018-07-14T05:23:45Z&operation=mean', headers=headers)
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
    assert record[3] == 'http://localhost/v1/meteocat/data/measure/AA/T?date=2018-07-14T05:23:45Z&operation=mean'
    assert record[4] == 'GET'
    assert json.loads(record[5]) == {"date": "2018-07-14T05:23:45Z", "operation": "mean"}
    assert record[6] == 400


def test_api_meteocat_data_measure_parameters_11(api, postgresql_schema):
    """
    Tests the nearest station with incomplete average operation parameter.

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8"))}
    response = api.get('/v1/meteocat/data/measure/AA/T?date=2018-07-14T05:23:45Z&operation=average', headers=headers)
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
    assert record[3] == 'http://localhost/v1/meteocat/data/measure/AA/T?date=2018-07-14T05:23:45Z&operation=average'
    assert record[4] == 'GET'
    assert json.loads(record[5]) == {"date": "2018-07-14T05:23:45Z", "operation": "average"}
    assert record[6] == 400


def test_api_meteocat_data_measure_parameters_12(api, postgresql_schema):
    """
    Tests the nearest station with exceeding average operation parameters.

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8"))}
    response = api.get('/v1/meteocat/data/measure/AA/T?date=2018-07-14T05:23:45Z&operation=average,5,78', headers=headers)
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
    assert record[3] == 'http://localhost/v1/meteocat/data/measure/AA/T?date=2018-07-14T05:23:45Z&operation=average,5,78'
    assert record[4] == 'GET'
    assert json.loads(record[5]) == {"date": "2018-07-14T05:23:45Z", "operation": "average,5,78"}
    assert record[6] == 400


def test_api_meteocat_data_measure_parameters_13(api, postgresql_schema):
    """
    Tests the nearest station with incorrect average operation parameters.

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8"))}
    response = api.get('/v1/meteocat/data/measure/AA/T?date=2018-07-14T05:23:45Z&operation=average,one_day', headers=headers)
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
    assert record[3] == 'http://localhost/v1/meteocat/data/measure/AA/T?date=2018-07-14T05:23:45Z&operation=average,one_day'
    assert record[4] == 'GET'
    assert json.loads(record[5]) == {"date": "2018-07-14T05:23:45Z", "operation": "average,one_day"}
    assert record[6] == 400


def test_api_meteocat_data_measure_parameters_14(api, postgresql_schema):
    """
    Tests the nearest station with correct parameters but not existing station.

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8"))}
    response = api.get('/v1/meteocat/data/measure/ZZTOP/T?date=2018-07-14T05:23:45Z&operation=average,5', headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 400
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 2
    assert data['status_code'] == 400
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 1
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    record = cursor.fetchone()
    assert record[1] == 3
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/meteocat/data/measure/ZZTOP/T?date=2018-07-14T05:23:45Z&operation=average,5'
    assert record[4] == 'GET'
    assert json.loads(record[5]) == {"date": "2018-07-14T05:23:45Z", "operation": "average,5"}
    assert record[6] == 400


def test_api_meteocat_data_measure_parameters_15(api, postgresql_schema):
    """
    Tests the nearest station with correct parameter but station is dismantled.

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8"))}
    response = api.get('/v1/meteocat/data/measure/UR/T?date=2018-07-14T05:23:45Z&operation=average,5', headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 400
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 2
    assert data['status_code'] == 400
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 1
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    record = cursor.fetchone()
    assert record[1] == 3
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/meteocat/data/measure/UR/T?date=2018-07-14T05:23:45Z&operation=average,5'
    assert record[4] == 'GET'
    assert json.loads(record[5]) == {"date": "2018-07-14T05:23:45Z", "operation": "average,5"}
    assert record[6] == 400


def test_api_meteocat_data_measure_parameters_16(api, postgresql_schema):
    """
    Tests the nearest station with correct parameter but not existing variable.

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8"))}
    response = api.get('/v1/meteocat/data/measure/DJ/ZZTOP?date=2018-07-14T05:23:45Z&operation=average,5', headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 400
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 2
    assert data['status_code'] == 400
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 1
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    record = cursor.fetchone()
    assert record[1] == 3
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/meteocat/data/measure/DJ/ZZTOP?date=2018-07-14T05:23:45Z&operation=average,5'
    assert record[4] == 'GET'
    assert json.loads(record[5]) == {"date": "2018-07-14T05:23:45Z", "operation": "average,5"}
    assert record[6] == 400


def test_api_meteocat_data_measure_parameters_17(api, postgresql_schema):
    """
    Tests the nearest station with correct parameter but not existing variable.

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8"))}
    response = api.get('/v1/meteocat/data/measure/DG/DV10?date=2006-07-14T05:23:45Z', headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 400
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 2
    assert data['status_code'] == 400
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 1
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    record = cursor.fetchone()
    assert record[1] == 3
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/meteocat/data/measure/DG/DV10?date=2006-07-14T05:23:45Z'
    assert record[4] == 'GET'
    assert json.loads(record[5]) == {"date": "2006-07-14T05:23:45Z"}
    assert record[6] == 400


def test_api_meteocat_data_measure_parameters_18(api, postgresql_schema):
    """
    Tests the measure with negative days average.

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8"))}
    response = api.get('/v1/meteocat/data/measure/DJ/ZZTOP?date=2018-07-14T05:23:45Z&operation=average,-5', headers=headers)
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
    assert record[3] == 'http://localhost/v1/meteocat/data/measure/DJ/ZZTOP?date=2018-07-14T05:23:45Z&operation=average,-5'
    assert record[4] == 'GET'
    assert json.loads(record[5]) == {"date": "2018-07-14T05:23:45Z", "operation": "average,-5"}
    assert record[6] == 400


def test_api_meteocat_data_measure_value_01(api, postgresql_schema):
    """
    Tests the read of one measure

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8"))}
    response = api.get('/v1/meteocat/data/measure/DJ/T?date=2018-07-14T05:23:45Z', headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 5
    assert data['date'] == "2018-07-14T05:00UTC"
    assert data['date_extreme'] is None
    assert data['value'] == 21.4
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 1
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    record = cursor.fetchone()
    assert record[1] == 3
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/meteocat/data/measure/DJ/T?date=2018-07-14T05:23:45Z'
    assert record[4] == 'GET'
    assert json.loads(record[5]) == {"date": "2018-07-14T05:23:45Z"}
    assert record[6] == 200


def test_api_meteocat_data_measure_value_02(api, postgresql_schema):
    """
    Tests the read of one measure that does not exist

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8"))}
    response = api.get('/v1/meteocat/data/measure/DJ/T?date=2019-07-14T05:23:45Z', headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 400
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 2
    assert data['status_code'] == 400
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 1
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    record = cursor.fetchone()
    assert record[1] == 3
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/meteocat/data/measure/DJ/T?date=2019-07-14T05:23:45Z'
    assert record[4] == 'GET'
    assert json.loads(record[5]) == {"date": "2019-07-14T05:23:45Z"}
    assert record[6] == 400


def test_api_meteocat_data_measure_average_value_01(api, postgresql_schema):
    """
    Tests the average of several measures

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8"))}
    response = api.get('/v1/meteocat/data/measure/DJ/T?date=2018-07-14T05:23:45Z&operation=average,1', headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 5
    assert data['date'] == "2018-07-14T05:23UTC"
    assert data['date_extreme'] is None
    assert data['value'] == 26.045833333333334
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 1
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    record = cursor.fetchone()
    assert record[1] == 3
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/meteocat/data/measure/DJ/T?date=2018-07-14T05:23:45Z&operation=average,1'
    assert record[4] == 'GET'
    assert json.loads(record[5]) == {"date": "2018-07-14T05:23:45Z", "operation": "average,1"}
    assert record[6] == 200


def test_api_meteocat_data_measure_average_value_02(api, postgresql_schema):
    """
    Tests the average of several measures

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8"))}
    response = api.get('/v1/meteocat/data/measure/DJ/T?date=2019-07-14T05:23:45Z&operation=average,1', headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 400
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 2
    assert data['status_code'] == 400
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 1
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    record = cursor.fetchone()
    assert record[1] == 3
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/meteocat/data/measure/DJ/T?date=2019-07-14T05:23:45Z&operation=average,1'
    assert record[4] == 'GET'
    assert json.loads(record[5]) == {"date": "2019-07-14T05:23:45Z", "operation": "average,1"}
    assert record[6] == 400


def test_api_meteocat_data_measure_sum_value_01(api, postgresql_schema):
    """
    Tests the average of several measures

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8"))}
    response = api.get('/v1/meteocat/data/measure/DJ/PPT?date=2018-07-14T05:23:45Z&operation=sum,1', headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 5
    assert data['date'] == "2018-07-14T05:23UTC"
    assert data['date_extreme'] is None
    assert data['value'] == 26.045833333333334
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 1
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    record = cursor.fetchone()
    assert record[1] == 3
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/meteocat/data/measure/DJ/PPT?date=2018-07-14T05:23:45Z&operation=sum,1'
    assert record[4] == 'GET'
    assert json.loads(record[5]) == {"date": "2018-07-14T05:23:45Z", "operation": "sum,1"}
    assert record[6] == 200


