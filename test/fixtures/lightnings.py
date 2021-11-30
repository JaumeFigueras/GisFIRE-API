#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest


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
