#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
import json


@pytest.fixture(scope='session')
def lightnings_meteocat_xdde_api_error():
    return {'status_code': 400,
            'data': {"message": "La data 2021-10-21T236:00Z no té el format YYYY-MM-DD[T]HH:mm[Z] o no existeix",
                     "aws": {"logGroupName": "/aws/lambda/api-xdde-pro-getLlampsCatalunya",
                             "logStreamName": "2021/11/11/[$LATEST]55a30f87a1c44f7c8de98dedfb3b2608",
                             "functionName": "api-xdde-pro-getLlampsCatalunya",
                             "awsRequestId": "69b71aae-8aee-4b69-884b-09c56adc8b82"
                             }
                     }
            }


@pytest.fixture(scope='session')
def lightnings_meteocat_xdde_api_day4():
    return json.loads("""[
              {
                "id": 22449035,
                "data": "2021-11-04T08:45:00.868454Z",
                "correntPic": -137.455,
                "chi2": 0.40000001,
                "ellipse": {
                  "eixMajor": 4000,
                  "eixMenor": 600,
                  "angle": 51
                },
                "numSensors": 3,
                "nuvolTerra": true,
                "idMunicipi": "170144",
                "coordenades": {
                  "latitud": 42.407753,
                  "longitud": 2.7945485
                }
              },
              {
                "id": 22449041,
                "data": "2021-11-04T08:47:59.601066Z",
                "correntPic": -124.616,
                "chi2": 0.60000002,
                "ellipse": {
                  "eixMajor": 3900,
                  "eixMenor": 600,
                  "angle": 50
                },
                "numSensors": 3,
                "nuvolTerra": true,
                "idMunicipi": "171024",
                "coordenades": {
                  "latitud": 42.390556,
                  "longitud": 2.7464964
                }
              },
              {
                "id": 22449043,
                "data": "2021-11-04T08:58:16.984957Z",
                "correntPic": 37.4995,
                "chi2": 0.2,
                "ellipse": {
                  "eixMajor": 3800,
                  "eixMenor": 600,
                  "angle": 45.900002
                },
                "numSensors": 3,
                "nuvolTerra": true,
                "coordenades": {
                  "latitud": 42.361782,
                  "longitud": 2.6285126
                }
              }
            ]""")


@pytest.fixture(scope='session')
def lightnings_meteocat_xdde_api_day5():
    return json.loads("""[
              {
                "id": 22449035,
                "data": "2021-11-05T08:45:00.868454Z",
                "correntPic": -137.455,
                "chi2": 0.40000001,
                "ellipse": {
                  "eixMajor": 4000,
                  "eixMenor": 600,
                  "angle": 51
                },
                "numSensors": 3,
                "nuvolTerra": true,
                "idMunicipi": "170144",
                "coordenades": {
                  "latitud": 42.407753,
                  "longitud": 2.7945485
                }
              },
              {
                "id": 22449041,
                "data": "2021-11-05T08:47:59.601066Z",
                "correntPic": -124.616,
                "chi2": 0.60000002,
                "ellipse": {
                  "eixMajor": 3900,
                  "eixMenor": 600,
                  "angle": 50
                },
                "numSensors": 3,
                "nuvolTerra": true,
                "idMunicipi": "171024",
                "coordenades": {
                  "latitud": 42.390556,
                  "longitud": 2.7464964
                }
              },
              {
                "id": 22449043,
                "data": "2021-11-05T08:58:16.984957Z",
                "correntPic": 37.4995,
                "chi2": 0.2,
                "ellipse": {
                  "eixMajor": 3800,
                  "eixMenor": 600,
                  "angle": 45.900002
                },
                "numSensors": 3,
                "nuvolTerra": true,
                "coordenades": {
                  "latitud": 42.361782,
                  "longitud": 2.6285126
                }
              }
            ]""")


@pytest.fixture(scope='session')
def lightnings_meteocat_xdde_api_nothing():
    return json.loads('[]')

