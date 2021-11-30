#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from base64 import b64encode


def test_empty_api_auth_entrypoint_01(api, postgresql_schema):
    """
    Tests the auth entry point without action.

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    response = api.get('/v1/auth')
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
    assert record[3] == 'http://localhost/v1/auth'
    assert record[4] == 'GET'
    assert record[5] == '{}'
    assert record[6] == 500


def test_empty_api_auth_entrypoint_02(api, postgresql_schema):
    """
    Tests the auth entry point without action.

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    response = api.get('/v1/auth/')
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
    assert record[3] == 'http://localhost/v1/auth/'
    assert record[4] == 'GET'
    assert record[5] == '{}'
    assert record[6] == 500


def test_empty_api_auth_get_token_01(api, postgresql_schema):
    """
    Tests the get token action. Getting tokens is not supported, so it must fail
    (✔ - YES;  ❌ - NO; NA - Not Applicable)
    authorization
        - header: ❌
        - username: NA
        - password: NA
        - admin: NA

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    response = api.get('/v1/auth/token')
    assert response.content_type == 'application/json'
    assert response.status_code == 405
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 1
    assert data['status_code'] == 405
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 1
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    record = cursor.fetchone()
    assert record[1] is None
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/auth/token'
    assert record[4] == 'GET'
    assert record[5] == '{}'
    assert record[6] == 405


def test_empty_api_auth_get_token_02(api, postgresql_schema):
    """
    Tests the get token action. Getting tokens is not supported, so it must fail
    (✔ - YES;  ❌ - NO; NA - Not Applicable)
    authorization
        - header: ✔
        - username: ✔
        - password: ❌
        - admin: NA

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"john.doe:pepito").decode("utf-8"))}
    response = api.get('/v1/auth/token', headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 405
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 1
    assert data['status_code'] == 405
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 1
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    record = cursor.fetchone()
    assert record[1] is None
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/auth/token'
    assert record[4] == 'GET'
    assert record[5] == '{}'
    assert record[6] == 405


def test_empty_api_auth_get_token_03(api, postgresql_schema):
    """
    Tests the get token action. Getting tokens is not supported, so it must fail
    (✔ - YES;  ❌ - NO; NA - Not Applicable)
    authorization
        - header: ✔
        - username: ✔
        - password: ✔
        - admin: ❌

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8"))}
    response = api.get('/v1/auth/token', headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 405
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 1
    assert data['status_code'] == 405
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 1
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    record = cursor.fetchone()
    assert record[1] is None
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/auth/token'
    assert record[4] == 'GET'
    assert record[5] == '{}'
    assert record[6] == 405


def test_empty_api_auth_get_token_04(api, postgresql_schema):
    """
    Tests the get token action. Getting tokens is not supported, so it must fail
    (✔ - YES;  ❌ - NO; NA - Not Applicable)
    authorization
        - header: ✔
        - username: ✔
        - password: ✔
        - admin: ✔

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"john.doe:qwertyuiop123456789").decode("utf-8"))}
    response = api.get('/v1/auth/token', headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 405
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 1
    assert data['status_code'] == 405
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 1
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    record = cursor.fetchone()
    assert record[1] is None
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/auth/token'
    assert record[4] == 'GET'
    assert record[5] == '{}'
    assert record[6] == 405


def test_empty_api_auth_post_token_01(api, postgresql_schema):
    """
    Tests a new user POST with: (✔ - YES;  ❌ - NO; NA - Not Applicable)
        authorization
            - header: ❌
            - username: NA
            - password: NA
            - admin: NA
        parameters
            - params: ❌
            - username: NA
            - valid date: NA

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    response = api.post('/v1/auth/token')
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
    assert record[1] is None
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/auth/token'
    assert record[4] == 'POST'
    assert record[5] == '{}'
    assert record[6] == 401


def test_empty_api_auth_post_token_02(api, postgresql_schema):
    """
    Tests a new user POST with: (✔ - YES;  ❌ - NO; NA - Not Applicable)
        authorization
            - header: ✔
            - username: ❌
            - password: ❌
            - admin: NA
        parameters
            - params: ❌
            - username: NA
            - valid date: NA

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"username:password").decode("utf-8"))}
    response = api.post('/v1/auth/token', headers=headers)
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
    assert record[1] is None
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/auth/token'
    assert record[4] == 'POST'
    assert record[5] == '{}'
    assert record[6] == 401


def test_empty_api_auth_post_token_03(api, postgresql_schema):
    """
    Tests a new user POST with: (✔ - YES;  ❌ - NO; NA - Not Applicable)
        authorization
            - header: ✔
            - username: ❌
            - password: ✔
            - admin: NA
        parameters
            - params: ❌
            - username: NA
            - valid date: NA

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"username:qwertyuiop123456789").decode("utf-8"))}
    response = api.post('/v1/auth/token', headers=headers)
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
    assert record[1] is None
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/auth/token'
    assert record[4] == 'POST'
    assert record[5] == '{}'
    assert record[6] == 401


def test_empty_api_auth_post_token_04(api, postgresql_schema):
    """
    Tests a new user POST with: (✔ - YES;  ❌ - NO; NA - Not Applicable)
        authorization
            - header: ✔
            - username: ✔
            - password: ✔
            - admin: ❌
        parameters
            - params: ❌
            - username: NA
            - valid date: NA

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8"))}
    response = api.post('/v1/auth/token', headers=headers)
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
    assert record[1] is None
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/auth/token'
    assert record[4] == 'POST'
    assert record[5] == '{}'
    assert record[6] == 401


def test_empty_api_auth_post_token_05(api, postgresql_schema):
    """
    Tests a new user POST with: (✔ - YES;  ❌ - NO; NA - Not Applicable)
        authorization
            - header: ✔
            - username: ✔
            - password: ✔
            - admin: ✔
        parameters
            - params: ❌
            - username: NA
            - valid date: NA

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"john.doe:qwertyuiop123456789").decode("utf-8"))}
    response = api.post('/v1/auth/token', headers=headers)
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
    assert record[1] == 1
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/auth/token'
    assert record[4] == 'POST'
    assert record[5] == '{}'
    assert record[6] == 422


def test_empty_api_auth_post_token_06(api, postgresql_schema):
    """
    Tests a new user POST with: (✔ - YES;  ❌ - NO; NA - Not Applicable)
        authorization
            - header: ❌
            - username: NA
            - password: NA
            - admin: NA
        parameters
            - params: ✔
            - username: ✔
            - valid date: ✔

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    params = {'username': 'jack.jones', 'valid_until': '2022-01-01T00:00:00'}
    response = api.post('/v1/auth/token', data=params)
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
    assert record[1] is None
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/auth/token'
    assert record[4] == 'POST'
    assert json.loads(record[5]) == params
    assert record[6] == 401


def test_empty_api_auth_post_token_07(api, postgresql_schema):
    """
    Tests a new user POST with: (✔ - YES;  ❌ - NO; NA - Not Applicable)
        authorization
            - header: ✔
            - username: ✔
            - password: ✔
            - admin: ✔
        parameters
            - params: ✔
            - username: ❌
            - valid date: ❌

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"john.doe:qwertyuiop123456789").decode("utf-8"))}
    params = {'usernames': 'jack.jones', 'validity_until': '2022-01-01T00:00:00'}
    response = api.post('/v1/auth/token', headers=headers, data=params)
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
    assert record[1] == 1
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/auth/token'
    assert record[4] == 'POST'
    assert json.loads(record[5]) == params
    assert record[6] == 422


def test_empty_api_auth_post_token_08(api, postgresql_schema):
    """
    Tests a new user POST with: (✔ - YES;  ❌ - NO; NA - Not Applicable)
        authorization
            - header: ✔
            - username: ✔
            - password: ✔
            - admin: ✔
        parameters
            - params: ✔
            - username: ✔
            - valid date: ❌

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"john.doe:qwertyuiop123456789").decode("utf-8"))}
    params = {'username': 'jack.jones', 'validity_until': '2022-01-01T00:00:00'}
    response = api.post('/v1/auth/token', headers=headers, data=params)
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
    assert record[1] == 1
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/auth/token'
    assert record[4] == 'POST'
    assert json.loads(record[5]) == params
    assert record[6] == 422


def test_empty_api_auth_post_token_09(api, postgresql_schema):
    """
    Tests a new user POST with: (✔ - YES;  ❌ - NO; NA - Not Applicable)
        authorization
            - header: ✔
            - username: ✔
            - password: ✔
            - admin: ✔
        parameters
            - params: ✔
            - username: ❌
            - valid date: ✔

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"john.doe:qwertyuiop123456789").decode("utf-8"))}
    params = {'usernames': 'jack.jones', 'valid_until': '2022-01-01T00:00:00'}
    response = api.post('/v1/auth/token', headers=headers, data=params)
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
    assert record[1] == 1
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/auth/token'
    assert record[4] == 'POST'
    assert json.loads(record[5]) == params
    assert record[6] == 422


def test_empty_api_auth_post_token_10(api, postgresql_schema):
    """
    Tests a new user POST with: (✔ - YES;  ❌ - NO; NA - Not Applicable)
        authorization
            - header: ✔
            - username: ✔
            - password: ✔
            - admin: ❌
        parameters
            - params: ✔
            - username: ✔
            - valid date: ✔

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8"))}
    params = {'username': 'jack.jones', 'valid_until': '2022-01-01T00:00:00'}
    response = api.post('/v1/auth/token', headers=headers, data=params)
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
    assert record[1] is None
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/auth/token'
    assert record[4] == 'POST'
    assert json.loads(record[5]) == params
    assert record[6] == 401


def test_empty_api_auth_post_token_11(api, postgresql_schema):
    """
    Tests a new user POST with: (✔ - YES;  ❌ - NO; NA - Not Applicable)
        authorization
            - header: ✔
            - username: ✔
            - password: ✔
            - admin: ✔
        parameters
            - params: ✔
            - username: ✔
            - valid date: ✔

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"john.doe:qwertyuiop123456789").decode("utf-8"))}
    params = {'username': 'jack.jones', 'valid_until': '2022-01-01T00:00:00'}
    response = api.post('/v1/auth/token', headers=headers, data=params)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 3
    assert data['username'] == 'jack.jones'
    assert data['valid_until'] == '2022-01-01T00:00:00'
    assert len(data['token']) == 64
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 1
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    record = cursor.fetchone()
    assert record[1] == 1
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/auth/token'
    assert record[4] == 'POST'
    assert json.loads(record[5]) == params
    assert record[6] == 200


def test_empty_api_auth_post_token_12(api, postgresql_schema):
    """
    Tests a new user POST with: (✔ - YES;  ❌ - NO; NA - Not Applicable)
        authorization
            - header: ✔
            - username: ✔
            - password: ✔
            - admin: ✔
        parameters
            - params: ✔
            - username: ❌
            - valid date: ✔

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"john.doe:qwertyuiop123456789").decode("utf-8"))}
    params = {'usernames': 'jack.jones', 'valid_until': '2022-01-01T00:00:00'}
    response = api.post('/v1/auth/token', headers=headers, data=params)
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
    assert record[1] == 1
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/auth/token'
    assert record[4] == 'POST'
    assert json.loads(record[5]) == params
    assert record[6] == 422


def test_empty_api_auth_post_token_13(api, postgresql_schema):
    """
    Tests a new user POST with: (✔ - YES;  ❌ - NO; NA - Not Applicable)
        authorization
            - header: ✔
            - username: ✔
            - password: ✔
            - admin: ✔
        parameters
            - params: ✔
            - username: ✔
            - valid date: ❌

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"john.doe:qwertyuiop123456789").decode("utf-8"))}
    params = {'username': 'jack.jones', 'valid_until': '2022-01-01 00:00:00'}
    response = api.post('/v1/auth/token', headers=headers, data=params)
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
    assert record[1] == 1
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/auth/token'
    assert record[4] == 'POST'
    assert json.loads(record[5]) == params
    assert record[6] == 422


def test_empty_api_auth_post_token_14(api, postgresql_schema):
    """
    Tests a new user POST with: (✔ - YES;  ❌ - NO; NA - Not Applicable)
        authorization
            - header: ✔
            - username: ✔
            - password: ✔
            - admin: ✔
        parameters
            - params: ✔
            - username: ❌
            - valid date: ✔

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"john.doe:qwertyuiop123456789").decode("utf-8"))}
    params = {'username': 'jack.jones', 'valid_until': '2022-01-01T00:00:00'}
    response = api.post('/v1/auth/token', headers=headers, data=params)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    response = api.post('/v1/auth/token', headers=headers, data=params)
    assert response.content_type == 'application/json'
    assert response.status_code == 422
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 1
    assert data['status_code'] == 422
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 2
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    record = cursor.fetchone()
    assert record[1] == 1
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/auth/token'
    assert record[4] == 'POST'
    assert json.loads(record[5]) == params
    assert record[6] == 200
    record = cursor.fetchone()
    assert record[1] is None
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/auth/token'
    assert record[4] == 'POST'
    assert json.loads(record[5]) == params
    assert record[6] == 422


def test_empty_api_auth_put_token_01(api, postgresql_schema):
    """
    Tests a new user PUT with: (✔ - YES;  ❌ - NO; NA - Not Applicable)
        authorization
            - header: ❌
            - username: NA
            - password: NA
            - admin: NA
        parameters
            - params: ❌
            - username: NA
            - valid date: NA

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    response = api.put('/v1/auth/token')
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
    assert record[1] is None
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/auth/token'
    assert record[4] == 'PUT'
    assert record[5] == '{}'
    assert record[6] == 401


def test_empty_api_auth_put_token_02(api, postgresql_schema):
    """
    Tests a new user PUT with: (✔ - YES;  ❌ - NO; NA - Not Applicable)
        authorization
            - header: ✔
            - username: ❌
            - password: ❌
            - admin: NA
        parameters
            - params: ❌
            - username: NA
            - valid date: NA

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"username:password").decode("utf-8"))}
    response = api.put('/v1/auth/token', headers=headers)
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
    assert record[1] is None
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/auth/token'
    assert record[4] == 'PUT'
    assert record[5] == '{}'
    assert record[6] == 401


def test_empty_api_auth_put_token_03(api, postgresql_schema):
    """
    Tests a new user PUT with: (✔ - YES;  ❌ - NO; NA - Not Applicable)
        authorization
            - header: ✔
            - username: ❌
            - password: ✔
            - admin: NA
        parameters
            - params: ❌
            - username: NA
            - valid date: NA

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"username:qwertyuiop123456789").decode("utf-8"))}
    response = api.put('/v1/auth/token', headers=headers)
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
    assert record[1] is None
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/auth/token'
    assert record[4] == 'PUT'
    assert record[5] == '{}'
    assert record[6] == 401


def test_empty_api_auth_put_token_04(api, postgresql_schema):
    """
    Tests a new user PUT with: (✔ - YES;  ❌ - NO; NA - Not Applicable)
        authorization
            - header: ✔
            - username: ✔
            - password: ✔
            - admin: ❌
        parameters
            - params: ❌
            - username: NA
            - valid date: NA

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8"))}
    response = api.put('/v1/auth/token', headers=headers)
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
    assert record[1] is None
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/auth/token'
    assert record[4] == 'PUT'
    assert record[5] == '{}'
    assert record[6] == 401


def test_empty_api_auth_put_token_05(api, postgresql_schema):
    """
    Tests a new user PUT with: (✔ - YES;  ❌ - NO; NA - Not Applicable)
        authorization
            - header: ✔
            - username: ✔
            - password: ✔
            - admin: ✔
        parameters
            - params: ❌
            - username: NA
            - valid date: NA

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"john.doe:qwertyuiop123456789").decode("utf-8"))}
    response = api.put('/v1/auth/token', headers=headers)
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
    assert record[1] == 1
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/auth/token'
    assert record[4] == 'PUT'
    assert record[5] == '{}'
    assert record[6] == 422


def test_empty_api_auth_put_token_06(api, postgresql_schema):
    """
    Tests a new user PUT with: (✔ - YES;  ❌ - NO; NA - Not Applicable)
        authorization
            - header: ❌
            - username: NA
            - password: NA
            - admin: NA
        parameters
            - params: ✔
            - username: ✔
            - valid date: ✔

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    params = {'username': 'jack.jones', 'valid_until': '2022-01-01T00:00:00'}
    response = api.put('/v1/auth/token', data=params)
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
    assert record[1] is None
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/auth/token'
    assert record[4] == 'PUT'
    assert json.loads(record[5]) == params
    assert record[6] == 401


def test_empty_api_auth_put_token_07(api, postgresql_schema):
    """
    Tests a new user PUT with: (✔ - YES;  ❌ - NO; NA - Not Applicable)
        authorization
            - header: ✔
            - username: ✔
            - password: ✔
            - admin: ✔
        parameters
            - params: ✔
            - username: ❌
            - valid date: ❌

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"john.doe:qwertyuiop123456789").decode("utf-8"))}
    params = {'usernames': 'jack.jones', 'validity_until': '2022-01-01T00:00:00'}
    response = api.put('/v1/auth/token', headers=headers, data=params)
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
    assert record[1] == 1
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/auth/token'
    assert record[4] == 'PUT'
    assert json.loads(record[5]) == params
    assert record[6] == 422


def test_empty_api_auth_put_token_08(api, postgresql_schema):
    """
    Tests a new user PUT with: (✔ - YES;  ❌ - NO; NA - Not Applicable)
        authorization
            - header: ✔
            - username: ✔
            - password: ✔
            - admin: ✔
        parameters
            - params: ✔
            - username: ✔
            - valid date: ❌

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"john.doe:qwertyuiop123456789").decode("utf-8"))}
    params = {'username': 'jack.jones', 'validity_until': '2022-01-01T00:00:00'}
    response = api.put('/v1/auth/token', headers=headers, data=params)
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
    assert record[1] == 1
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/auth/token'
    assert record[4] == 'PUT'
    assert json.loads(record[5]) == params
    assert record[6] == 422


def test_empty_api_auth_put_token_09(api, postgresql_schema):
    """
    Tests a new user PUT with: (✔ - YES;  ❌ - NO; NA - Not Applicable)
        authorization
            - header: ✔
            - username: ✔
            - password: ✔
            - admin: ✔
        parameters
            - params: ✔
            - username: ❌
            - valid date: ✔

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"john.doe:qwertyuiop123456789").decode("utf-8"))}
    params = {'usernames': 'jack.jones', 'valid_until': '2022-01-01T00:00:00'}
    response = api.put('/v1/auth/token', headers=headers, data=params)
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
    assert record[1] == 1
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/auth/token'
    assert record[4] == 'PUT'
    assert json.loads(record[5]) == params
    assert record[6] == 422


def test_empty_api_auth_put_token_10(api, postgresql_schema):
    """
    Tests a new user PUT with: (✔ - YES;  ❌ - NO; NA - Not Applicable)
        authorization
            - header: ✔
            - username: ✔
            - password: ✔
            - admin: ❌
        parameters
            - params: ✔
            - username: ✔
            - valid date: ✔

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8"))}
    params = {'username': 'jack.jones', 'valid_until': '2022-01-01T00:00:00'}
    response = api.put('/v1/auth/token', headers=headers, data=params)
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
    assert record[1] is None
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/auth/token'
    assert record[4] == 'PUT'
    assert json.loads(record[5]) == params
    assert record[6] == 401


def test_empty_api_auth_put_token_11(api, postgresql_schema):
    """
    Tests a new user PUT with: (✔ - YES;  ❌ - NO; NA - Not Applicable)
        authorization
            - header: ✔
            - username: ✔
            - password: ✔
            - admin: ✔
        parameters
            - params: ✔
            - username: ❌
            - valid date: ✔

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"john.doe:qwertyuiop123456789").decode("utf-8"))}
    params = {'username': 'jack.jones', 'valid_until': '2022-01-01T00:00:00'}
    response = api.put('/v1/auth/token', headers=headers, data=params)
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
    assert record[1] == 1
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/auth/token'
    assert record[4] == 'PUT'
    assert json.loads(record[5]) == params
    assert record[6] == 422


def test_empty_api_auth_put_token_12(api, postgresql_schema):
    """
    Tests a new user PUT with: (✔ - YES;  ❌ - NO; NA - Not Applicable)
        authorization
            - header: ✔
            - username: ✔
            - password: ✔
            - admin: ✔
        parameters
            - params: ✔
            - username: ✔
            - valid date: ✔

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"john.doe:qwertyuiop123456789").decode("utf-8"))}
    params = {'username': 'jack.jones', 'valid_until': '2022-01-01T00:00:00'}
    response = api.post('/v1/auth/token', headers=headers, data=params)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 3
    assert data['username'] == 'jack.jones'
    assert data['valid_until'] == '2022-01-01T00:00:00'
    assert len(data['token']) == 64
    params = {'username': 'jack.jones', 'valid_until': '2023-01-01T00:00:00'}
    response = api.put('/v1/auth/token', headers=headers, data=params)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 3
    assert data['username'] == 'jack.jones'
    assert data['valid_until'] == '2023-01-01T00:00:00'
    assert len(data['token']) == 64
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 2
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    record = cursor.fetchone()
    assert record[1] == 1
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/auth/token'
    assert record[4] == 'POST'
    assert json.loads(record[5]) == {'username': 'jack.jones', 'valid_until': '2022-01-01T00:00:00'}
    assert record[6] == 200
    record = cursor.fetchone()
    assert record[1] == 1
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/auth/token'
    assert record[4] == 'PUT'
    assert json.loads(record[5]) == {'username': 'jack.jones', 'valid_until': '2023-01-01T00:00:00'}
    assert record[6] == 200


def test_empty_api_auth_put_token_13(api, postgresql_schema):
    """
    Tests a new user PUT with: (✔ - YES;  ❌ - NO; NA - Not Applicable)
        authorization
            - header: ✔
            - username: ✔
            - password: ✔
            - admin: ✔
        parameters
            - params: ✔
            - username: ✔
            - valid date: ❌

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"john.doe:qwertyuiop123456789").decode("utf-8"))}
    params = {'username': 'jack.jones', 'valid_until': '2022-01-01T00:00:00'}
    response = api.post('/v1/auth/token', headers=headers, data=params)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 3
    assert data['username'] == 'jack.jones'
    assert data['valid_until'] == '2022-01-01T00:00:00'
    assert len(data['token']) == 64
    params = {'username': 'jack.jones', 'valid_until': '2023-01-01 00:00:00'}
    response = api.put('/v1/auth/token', headers=headers, data=params)
    assert response.content_type == 'application/json'
    assert response.status_code == 422
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 1
    assert data['status_code'] == 422
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 2
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    record = cursor.fetchone()
    assert record[1] == 1
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/auth/token'
    assert record[4] == 'POST'
    assert json.loads(record[5]) == {'username': 'jack.jones', 'valid_until': '2022-01-01T00:00:00'}
    assert record[6] == 200
    record = cursor.fetchone()
    assert record[1] == 1
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/auth/token'
    assert record[4] == 'PUT'
    assert json.loads(record[5]) == {'username': 'jack.jones', 'valid_until': '2023-01-01 00:00:00'}
    assert record[6] == 422


def test_empty_api_auth_delete_token_01(api, postgresql_schema):
    """
    Tests a new user DELETE with: (✔ - YES;  ❌ - NO; NA - Not Applicable)
        authorization
            - header: ❌
            - username: NA
            - password: NA
            - admin: NA
        parameters
            - params: ❌
            - username: NA

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    response = api.delete('/v1/auth/token')
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
    assert record[1] is None
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/auth/token'
    assert record[4] == 'DELETE'
    assert record[5] == '{}'
    assert record[6] == 401


def test_empty_api_auth_delete_token_02(api, postgresql_schema):
    """
    Tests a new user DELETE with: (✔ - YES;  ❌ - NO; NA - Not Applicable)
        authorization
            - header: ✔
            - username: ❌
            - password: ❌
            - admin: NA
        parameters
            - params: ❌
            - username: NA

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"username:password").decode("utf-8"))}
    response = api.delete('/v1/auth/token', headers=headers)
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
    assert record[1] is None
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/auth/token'
    assert record[4] == 'DELETE'
    assert record[5] == '{}'
    assert record[6] == 401


def test_empty_api_auth_delete_token_03(api, postgresql_schema):
    """
    Tests a new user DELETE with: (✔ - YES;  ❌ - NO; NA - Not Applicable)
        authorization
            - header: ✔
            - username: ❌
            - password: ✔
            - admin: NA
        parameters
            - params: ❌
            - username: NA

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"username:qwertyuiop123456789").decode("utf-8"))}
    response = api.delete('/v1/auth/token', headers=headers)
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
    assert record[1] is None
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/auth/token'
    assert record[4] == 'DELETE'
    assert record[5] == '{}'
    assert record[6] == 401


def test_empty_api_auth_delete_token_04(api, postgresql_schema):
    """
    Tests a new user DELETE with: (✔ - YES;  ❌ - NO; NA - Not Applicable)
        authorization
            - header: ✔
            - username: ✔
            - password: ✔
            - admin: ❌
        parameters
            - params: ❌
            - username: NA

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8"))}
    response = api.delete('/v1/auth/token', headers=headers)
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
    assert record[1] is None
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/auth/token'
    assert record[4] == 'DELETE'
    assert record[5] == '{}'
    assert record[6] == 401


def test_empty_api_auth_delete_token_05(api, postgresql_schema):
    """
    Tests a new user DELETE with: (✔ - YES;  ❌ - NO; NA - Not Applicable)
        authorization
            - header: ✔
            - username: ✔
            - password: ✔
            - admin: ✔
        parameters
            - params: ❌
            - username: NA
            - valid date: NA

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"john.doe:qwertyuiop123456789").decode("utf-8"))}
    response = api.delete('/v1/auth/token', headers=headers)
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
    assert record[1] == 1
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/auth/token'
    assert record[4] == 'DELETE'
    assert record[5] == '{}'
    assert record[6] == 422


def test_empty_api_auth_delete_token_06(api, postgresql_schema):
    """
    Tests a new user DELETE with: (✔ - YES;  ❌ - NO; NA - Not Applicable)
        authorization
            - header: ❌
            - username: NA
            - password: NA
            - admin: NA
        parameters
            - params: ✔
            - username: ✔

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    params = {'username': 'jack.jones', 'valid_until': '2022-01-01T00:00:00'}
    response = api.delete('/v1/auth/token', data=params)
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
    assert record[1] is None
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/auth/token'
    assert record[4] == 'DELETE'
    assert json.loads(record[5]) == params
    assert record[6] == 401


def test_empty_api_auth_delete_token_07(api, postgresql_schema):
    """
    Tests a new user DELETE with: (✔ - YES;  ❌ - NO; NA - Not Applicable)
        authorization
            - header: ✔
            - username: ✔
            - password: ✔
            - admin: ✔
        parameters
            - params: ✔
            - username: ❌

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"john.doe:qwertyuiop123456789").decode("utf-8"))}
    params = {'usernames': 'jack.jones'}
    response = api.delete('/v1/auth/token', headers=headers, data=params)
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
    assert record[1] == 1
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/auth/token'
    assert record[4] == 'DELETE'
    assert json.loads(record[5]) == params
    assert record[6] == 422


def test_empty_api_auth_delete_token_08(api, postgresql_schema):
    """
    Tests a new user DELETE with: (✔ - YES;  ❌ - NO; NA - Not Applicable)
        authorization
            - header: ✔
            - username: ✔
            - password: ✔
            - admin: ✔
        parameters
            - params: ✔
            - username: ❌ (but not existing)

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"john.doe:qwertyuiop123456789").decode("utf-8"))}
    params = {'username': 'jack.jones'}
    response = api.delete('/v1/auth/token', headers=headers, data=params)
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
    assert record[1] == 1
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/auth/token'
    assert record[4] == 'DELETE'
    assert json.loads(record[5]) == params
    assert record[6] == 422


def test_empty_api_auth_delete_token_09(api, postgresql_schema):
    """
    Tests a new user DELETE with: (✔ - YES;  ❌ - NO; NA - Not Applicable)
        authorization
            - header: ✔
            - username: ✔
            - password: ✔
            - admin: ✔
        parameters
            - params: ✔
            - username: ✔

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"john.doe:qwertyuiop123456789").decode("utf-8"))}
    params = {'username': 'jack.jones', 'valid_until': '2022-01-01T00:00:00'}
    response = api.post('/v1/auth/token', headers=headers, data=params)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 3
    assert data['username'] == 'jack.jones'
    assert data['valid_until'] == '2022-01-01T00:00:00'
    assert len(data['token']) == 64
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"john.doe:qwertyuiop123456789").decode("utf-8"))}
    params = {'username': 'jack.jones'}
    response = api.delete('/v1/auth/token', headers=headers, data=params)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 0
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 2
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    _ = cursor.fetchone()
    record = cursor.fetchone()
    assert record[1] == 1
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/auth/token'
    assert record[4] == 'DELETE'
    assert json.loads(record[5]) == params
    assert record[6] == 200


def test_empty_api_auth_delete_token_10(api, postgresql_schema):
    """
    Tests a new user DELETE with: (✔ - YES;  ❌ - NO; NA - Not Applicable)
        authorization
            - header: ✔
            - username: ✔
            - password: ✔
            - admin: ❌
        parameters
            - params: ✔
            - username: ✔
            - valid date: ✔

    :param api: Flask API fixture
    :return: None
    """
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    count = record[0]
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"john.doe:qwertyuiop123456789").decode("utf-8"))}
    params = {'username': 'jack.jones', 'valid_until': '2022-01-01T00:00:00'}
    response = api.post('/v1/auth/token', headers=headers, data=params)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 3
    assert data['username'] == 'jack.jones'
    assert data['valid_until'] == '2022-01-01T00:00:00'
    assert len(data['token']) == 64
    headers = {'Authorization': 'Basic {}'.format(b64encode(b"jack.skellington:0123456789asdfghjkl").decode("utf-8"))}
    params = {'username': 'jack.jones'}
    response = api.delete('/v1/auth/token', headers=headers, data=params)
    assert response.content_type == 'application/json'
    assert response.status_code == 401
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 1
    assert data['status_code'] == 401
    cursor = postgresql_schema.cursor()
    cursor.execute("SELECT count(*) FROM user_access")
    record = cursor.fetchone()
    assert record[0] == count + 2
    cursor.execute("SELECT id, user_id, ip, url, method, params, result_code FROM user_access")
    record = cursor.fetchone()
    record = cursor.fetchone()
    assert record[1] is None
    assert record[2] == '127.0.0.1'
    assert record[3] == 'http://localhost/v1/auth/token'
    assert record[4] == 'DELETE'
    assert json.loads(record[5]) == params
    assert record[6] == 401

