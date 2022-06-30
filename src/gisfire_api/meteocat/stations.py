#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import jsonify
from flask import request
from flask import current_app as app
from .. import db
from ..auth import auth
from ..user import UserAccess
from gisfire_meteocat_lib.remote_api import meteocat_xdde_api
from gisfire_meteocat_lib.classes.lightning import Lightning
from gisfire_meteocat_lib.classes.lightning import LightningAPIRequest
from requests.exceptions import RequestException
from sqlalchemy import func
import json
import pytz
import datetime

from typing import List
from typing import Tuple

bp = Blueprint("meteocat_stations", __name__, url_prefix="/v1/meteocat/stations")


@bp.route('/')
@bp.route('')
def main():
    """
    TODO:

    :return:
    """
    UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
               auth.current_user()).record_access(db, 500)
    return jsonify(status_code=500), 500


@bp.route('/nearest', methods=['GET'])
@bp.route('/nearest/', methods=['GET'])
@auth.login_required(role='user')
def get_nearest_weather_station():
    """
    TODO:

    :return:
    :rtype:
    """
    # Check we have basic parameters
    if (request.values is None) or ('date' not in request.values) or ('srid' not in request.values) or \
            (len(request.values) != 4):
        UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                   auth.current_user()).record_access(db, 422)
        return jsonify(status_code=422), 422
    # Check lat-lon or x-y pairs
    if not ((('lat' in request.values) and ('lon' in request.values)) or
            (('x' in request.values) and ('y' in request.values))):
        UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                   auth.current_user()).record_access(db, 422)
        return jsonify(status_code=422), 422
    pass



"""SELECT meteocat_weather_station._codi, 
  ST_Transform(meteocat_weather_station.geom, 25831) <-> ST_Transform('SRID=4258;POINT(0.62839 41.7145)', 25831) AS dist
FROM meteocat_weather_station, meteocat_weather_station_state 
WHERE meteocat_weather_station.id = meteocat_weather_station_state.meteocat_weather_station_id
  AND meteocat_weather_station_state._codi = 'ACTIVE'
  AND meteocat_weather_station_state._data_inici <= '2018-01-01T15:00:00Z'
  AND (meteocat_weather_station_state._data_fi >= '2018-01-01T15:00:00Z' 
       OR meteocat_weather_station_state._data_fi IS NULL)
ORDER BY dist
;"""