#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from base64 import b64encode
from freezegun import freeze_time
from gisfire_meteocat_lib.remote_api import meteocat_urls
from gisfire_meteocat_lib.remote_api import meteocat_api
import requests
import json


def test_empty_api_meteocat_lightning_entrypoint_01(api, postgresql_schema):
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
    :param postgresql_schema: Database fixture
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
    :param postgresql_schema: Database fixture
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
    :param postgresql_schema: Database fixture
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


def test_api_meteocat_lightning_other_day_01(api, postgresql_schema):
    """
    Tests a day with recorded previous queries all successful that have stored information in the database

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
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


def test_api_meteocat_lightning_other_day_02(api, postgresql_schema):
    """
    Tests a day that has not been requested and there i no data in the database. External requests have to be sent, but
    there is no token for the meteocat API in the headers

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
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


def test_api_meteocat_lightning_other_day_03(api, postgresql_schema, requests_mock, lightnings_meteocat_xdde_api_error):
    """
    Tests a day that has not been requested and there i no data in the database. The first throw an error and a 400 http
    status code is received

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
    :param requests_mock: Requests mock to simulate the MeteoCat API Responses
    :param lightnings_meteocat_xdde_api_error: Return of a failed Meteocat API call
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


def test_api_meteocat_lightning_other_day_04(api, postgresql_schema):
    """
    Tests a day that has been requested and there is no data in the database. The problem is that although the system
    says it has lightnings recorded there do not appear in the database

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
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
    response = api.get('/v1/meteocat/lightning/2021/11/03', headers=headers)
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
    assert record[1] == 3
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/meteocat/lightning/2021/11/03'
    assert record[4] == 'GET'
    assert record[5] == '{}'
    assert record[6] == 500
    cursor.execute("SELECT COUNT(*) FROM meteocat_xdde_request")
    record = cursor.fetchone()
    assert record[0] == count_reqs


def test_api_meteocat_lightning_other_day_05(api, postgresql_schema, requests_mock,
                                             lightnings_meteocat_xdde_api_nothing, lightnings_meteocat_xdde_api_day4):
    """
    Tests a new day that has no data in the database.

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
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
    cursor.execute("SELECT COUNT(*) FROM meteocat_lightning")
    record = cursor.fetchone()
    count_light = record[0]
    headers = {
        'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8")),
        'X-Api-Key': '1234'
    }
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 0)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 1)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 2)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 3)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 4)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 5)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 6)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 7)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 8)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_day4, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 9)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 10)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 11)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 12)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 13)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 14)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 15)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 16)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 17)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 18)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 19)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 20)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 21)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 22)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 23)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    response = api.get('/v1/meteocat/lightning/2021/11/04', headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 3
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 1
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    record = cursor.fetchone()
    assert record[1] == 3
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/meteocat/lightning/2021/11/04'
    assert record[4] == 'GET'
    assert record[5] == '{}'
    assert record[6] == 200
    cursor.execute("SELECT COUNT(*) FROM meteocat_xdde_request")
    record = cursor.fetchone()
    assert record[0] == count_reqs + 24
    cursor.execute("SELECT COUNT(*) FROM meteocat_lightning")
    record = cursor.fetchone()
    assert record[0] == count_light + 3


def test_api_meteocat_lightning_other_day_06(api, postgresql_schema, requests_mock,
                                             lightnings_meteocat_xdde_api_nothing, lightnings_meteocat_xdde_api_day4):
    """
    Tests a new day that has no data in the database. There is a timeout exception after the lightnings response.

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
    :return: None
    """
    meteocat_api.TIMEOUT = 0.1
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT COUNT(*) FROM meteocat_xdde_request")
    record = cursor.fetchone()
    count_reqs = record[0]
    cursor.execute("SELECT COUNT(*) FROM meteocat_lightning")
    record = cursor.fetchone()
    count_light = record[0]
    headers = {
        'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8")),
        'X-Api-Key': '1234'
    }
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 0)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 1)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 2)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 3)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 4)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 5)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 6)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 7)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 8)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_day4, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 9)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 10)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 11)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 12)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 13)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 14)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 15)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 16)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 17)
    requests_mock.get(url, exc=requests.exceptions.ConnectTimeout)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 18)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 19)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 20)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 21)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 22)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 4, 23)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    response = api.get('/v1/meteocat/lightning/2021/11/04', headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 500
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 1
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 1
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    record = cursor.fetchone()
    assert record[1] == 3
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/meteocat/lightning/2021/11/04'
    assert record[4] == 'GET'
    assert record[5] == '{}'
    assert record[6] == 500
    cursor.execute("SELECT COUNT(*) FROM meteocat_xdde_request")
    record = cursor.fetchone()
    assert record[0] == count_reqs + 17
    cursor.execute("SELECT COUNT(*) FROM meteocat_lightning")
    record = cursor.fetchone()
    assert record[0] == count_light + 3
    meteocat_api.TIMEOUT = 5


def test_api_meteocat_lightning_other_day_07(api, postgresql_schema, requests_mock,
                                             lightnings_meteocat_xdde_api_nothing, lightnings_meteocat_xdde_api_day5):
    """
    Tests a new day that has no data in the database. There is a timeout exception after the lightnings response.

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
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
    cursor.execute("SELECT COUNT(*) FROM meteocat_lightning")
    record = cursor.fetchone()
    count_light = record[0]
    headers = {
        'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8")),
        'X-Api-Key': '1234'
    }
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 5, 8)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_day5, status_code=200)
    response = api.get('/v1/meteocat/lightning/2021/11/05', headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 3
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 1
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    record = cursor.fetchone()
    assert record[1] == 3
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/meteocat/lightning/2021/11/05'
    assert record[4] == 'GET'
    assert record[5] == '{}'
    assert record[6] == 200
    cursor.execute("SELECT COUNT(*) FROM meteocat_xdde_request")
    record = cursor.fetchone()
    assert record[0] == count_reqs
    cursor.execute("SELECT * FROM meteocat_xdde_request WHERE request_date = '2021-11-05 08:00:00Z'")
    record = cursor.fetchone()
    assert record[1] == 200
    assert record[2] == 3
    cursor.execute("SELECT COUNT(*) FROM meteocat_lightning")
    record = cursor.fetchone()
    assert record[0] == count_light + 3


def test_api_meteocat_lightning_other_day_08(api, postgresql_schema, requests_mock,
                                             lightnings_meteocat_xdde_api_nothing, lightnings_meteocat_xdde_api_day5,
                                             lightnings_meteocat_xdde_api_error):
    """
    Tests a new day that has no data in the database. There is a timeout exception after the lightnings response.

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
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
    cursor.execute("SELECT COUNT(*) FROM meteocat_lightning")
    record = cursor.fetchone()
    count_light = record[0]
    headers = {
        'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8")),
        'X-Api-Key': '1234'
    }
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 5, 8)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_error, status_code=411)
    response = api.get('/v1/meteocat/lightning/2021/11/05', headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 411
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 1
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 1
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    record = cursor.fetchone()
    assert record[1] == 3
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/meteocat/lightning/2021/11/05'
    assert record[4] == 'GET'
    assert record[5] == '{}'
    assert record[6] == 411
    cursor.execute("SELECT COUNT(*) FROM meteocat_xdde_request")
    record = cursor.fetchone()
    assert record[0] == count_reqs
    cursor.execute("SELECT * FROM meteocat_xdde_request WHERE request_date = '2021-11-05 08:00:00Z'")
    record = cursor.fetchone()
    assert record[1] == 411
    assert record[2] is None
    cursor.execute("SELECT COUNT(*) FROM meteocat_lightning")
    record = cursor.fetchone()
    assert record[0] == count_light


@freeze_time("2021-11-02 08:25:33Z")
def test_api_meteocat_lightning_other_day_09(api, postgresql_schema, requests_mock,
                                             lightnings_meteocat_xdde_api_nothing):
    """
    Tests same day that has some data in the database.

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
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
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 2, 2)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 2, 3)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 2, 4)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 2, 5)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 2, 6)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 2, 7)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=200)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 2, 8)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=500)
    url = meteocat_urls.LIGHTNINGS_DATA.format(2021, 11, 2, 9)
    requests_mock.get(url, json=lightnings_meteocat_xdde_api_nothing, status_code=500)
    response = api.get('/v1/meteocat/lightning/2021/11/02', headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 5
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 1
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    record = cursor.fetchone()
    assert record[1] == 3
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/meteocat/lightning/2021/11/02'
    assert record[4] == 'GET'
    assert record[5] == '{}'
    assert record[6] == 200
    cursor.execute("SELECT COUNT(*) FROM meteocat_xdde_request")
    record = cursor.fetchone()
    assert record[0] == count_reqs + 5  # There are 6 requests but one is an update so only 5 more elements are added


@freeze_time("2021-11-02 00:25:33Z")
def test_api_meteocat_lightning_other_day_10(api, postgresql_schema, requests_mock):
    """
    Tests same day that has some data in the database.

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
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
    response = api.get('/v1/meteocat/lightning/2021/11/02', headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 0
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 1
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    record = cursor.fetchone()
    assert record[1] == 3
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/meteocat/lightning/2021/11/02'
    assert record[4] == 'GET'
    assert record[5] == '{}'
    assert record[6] == 200
    cursor.execute("SELECT COUNT(*) FROM meteocat_xdde_request")
    record = cursor.fetchone()
    assert record[0] == count_reqs


@freeze_time("2021-11-01 23:25:33Z")
def test_api_meteocat_lightning_other_day_11(api, postgresql_schema, requests_mock):
    """
    Tests same day that has some data in the database.

    :param api: Flask API fixture
    :param postgresql_schema: Database fixture
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
    response = api.get('/v1/meteocat/lightning/2021/11/02', headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 400
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 1
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 1
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    record = cursor.fetchone()
    assert record[1] == 3
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/meteocat/lightning/2021/11/02'
    assert record[4] == 'GET'
    assert record[5] == '{}'
    assert record[6] == 400
    cursor.execute("SELECT COUNT(*) FROM meteocat_xdde_request")
    record = cursor.fetchone()
    assert record[0] == count_reqs




