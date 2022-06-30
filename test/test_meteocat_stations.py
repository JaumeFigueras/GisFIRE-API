#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from base64 import b64encode
from freezegun import freeze_time
from gisfire_meteocat_lib.remote_api import meteocat_urls
from gisfire_meteocat_lib.remote_api import meteocat_api
import requests
import json


def test_empty_api_meteocat_stations_nearest_entrypoint_01(api, postgresql_schema):
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
    response = api.get('/v1/meteocat/stations/nearest/')
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

