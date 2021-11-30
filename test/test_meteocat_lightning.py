#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from base64 import b64encode
from freezegun import freeze_time
from gisfire_meteocat_lib.remote_api import meteocat_urls


def test_empty_api_meteocat_lightning_entrypoint_01(api, postgresql_schema):
    """
    Tests the auth entry point without action.

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    response = api.get('/v1/meteocat/lightning/')
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
    assert record[3] == 'http://localhost/v1/meteocat/lightning/'
    assert record[4] == 'GET'
    assert record[5] == '{}'
    assert record[6] == 500


def test_empty_api_meteocat_lightning_entrypoint_02(api, postgresql_schema):
    """
    Tests the auth entry point without action.

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    response = api.get('/v1/meteocat/lightning')
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
    assert record[3] == 'http://localhost/v1/meteocat/lightning'
    assert record[4] == 'GET'
    assert record[5] == '{}'
    assert record[6] == 500


def test_api_meteocat_lightning_wrong_date_01(api, postgresql_schema):
    """
    TODO:

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8"))}
    response = api.get('/v1/meteocat/lightning/2021/13/11', headers=headers)
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
    assert record[3] == 'http://localhost/v1/meteocat/lightning/2021/13/11'
    assert record[4] == 'GET'
    assert record[5] == '{}'
    assert record[6] == 422


def test_api_meteocat_lightning_wrong_date_02(api, postgresql_schema):
    """
    TODO:

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8"))}
    response = api.get('/v1/meteocat/lightning/2021/pepito/11', headers=headers)
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
    assert record[3] == 'http://localhost/v1/meteocat/lightning/2021/pepito/11'
    assert record[4] == 'GET'
    assert record[5] == '{}'
    assert record[6] == 404


@freeze_time("2021-11-02 08:00:00", tz_offset=+1)
def test_api_meteocat_lightning_other_day_01(api, postgresql_schema):
    """
    TODO:

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8"))}
    response = api.get('/v1/meteocat/lightning/2021/11/1', headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 3
    for elem in data:
        assert 'meteocat_id' in elem
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 1
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    record = cursor.fetchone()
    assert record[1] == 3
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/meteocat/lightning/2021/11/1'
    assert record[4] == 'GET'
    assert record[5] == '{}'
    assert record[6] == 200


@freeze_time("2021-11-02 08:00:00", tz_offset=+1)
def test_api_meteocat_lightning_other_day_02(api, postgresql_schema):
    """
    TODO:

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8"))}
    response = api.get('/v1/meteocat/lightning/2021/10/15', headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 401
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 1
    assert data['status_code'] == 401
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 1
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    record = cursor.fetchone()
    assert record[1] == 3
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/meteocat/lightning/2021/10/15'
    assert record[4] == 'GET'
    assert record[5] == '{}'
    assert record[6] == 401


@freeze_time("2021-11-02 08:00:00", tz_offset=+1)
def test_api_meteocat_lightning_other_day_03(api, postgresql_schema, requests_mock, lightnings_meteocat_xdde_api_error):
    """
    TODO:

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT COUNT(*) FROM meteocat_xdde_request")
    record = cursor.fetchone()
    count_reqs = record[0]
    headers = {
        'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8")),
        'X-Api-Key': '1234'
    }
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 10, 15, 0)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_error, status_code=400)
    response = api.get('/v1/meteocat/lightning/2021/10/15', headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 400
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 2
    assert data['status_code'] == 400
    assert data['message'] is None
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 1
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    record = cursor.fetchone()
    assert record[1] == 3
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/meteocat/lightning/2021/10/15'
    assert record[4] == 'GET'
    assert record[5] == '{}'
    assert record[6] == 400
    cursor.execute("SELECT COUNT(*) FROM meteocat_xdde_request")
    record = cursor.fetchone()
    assert record[0] == count_reqs + 1
    cursor.execute("SELECT * FROM meteocat_xdde_request WHERE request_date = '2021-10-15T00:00:00Z'")
    record = cursor.fetchone()
    assert record[1] == 400
    assert record[2] is None


