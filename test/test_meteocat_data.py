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
    Tests the nearest station with one wrong parameter.

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


def test_api_meteocat_data_measure_value_01(api, postgresql_schema):
    """
    Tests the nearest station with one wrong parameter.

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
    assert len(data) == 1
    assert data['status_code'] == 200
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
    assert json.loads(record[5]) == {"date": "2018-06-14T05:23:45Z"}
    assert record[6] == 200

