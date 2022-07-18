#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import jsonify
from flask import request
from flask import current_app as app
from .. import db
from ..auth import auth
from ..user import UserAccess
from gisfire_meteocat_lib.classes.weather_station import WeatherStation
from gisfire_meteocat_lib.classes.weather_station import WeatherStationState
from gisfire_meteocat_lib.classes.weather_station import WeatherStationStateCategory
from sqlalchemy import func
from sqlalchemy import or_
import json
import datetime
import dateutil.parser

from typing import List

bp = Blueprint("meteocat_stations", __name__, url_prefix="/v1/meteocat/station")


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


@bp.route('/nearest/', methods=['GET'])
@bp.route('/nearest', methods=['GET'])
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
    # Get the date
    date: str = request.values['date']
    try:
        date: datetime.datetime = dateutil.parser.isoparse(date)
    except ValueError as _:
        UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                   auth.current_user()).record_access(db, 400)
        return jsonify(status_code=400), 400
    # Get the SRID
    srid: str = request.values['srid']
    try:
        srid: int = int(srid)
    except ValueError as _:
        UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                   auth.current_user()).record_access(db, 400)
        return jsonify(status_code=400), 400
    # Get the Lon
    lon: str = request.values['lon'] if 'lon' in request.values else request.values['x']
    try:
        lon: float = float(lon)
    except ValueError as _:
        UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                   auth.current_user()).record_access(db, 400)
        return jsonify(status_code=400), 400
    # Get the Lon
    lat: str = request.values['lat'] if 'lon' in request.values else request.values['y']
    try:
        lat: float = float(lat)
    except ValueError as _:
        UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                   auth.current_user()).record_access(db, 400)
        return jsonify(status_code=400), 400
    # Query station
    station_with_distance: List[WeatherStation, float] = \
        db.session.query(WeatherStation, WeatherStation.postgis_geometry.distance_centroid(
            func.ST_Transform(func.ST_GeomFromEWKT('SRID={0:d};POINT({1:f} {2:f})'.format(srid, lon, lat)),
                              WeatherStation.SRID_WEATHER_STATIONS)).label('dist')). \
        join(WeatherStationState, WeatherStation.id == WeatherStationState.meteocat_weather_station_id). \
        filter(WeatherStationState.code == WeatherStationStateCategory.ACTIVE). \
        filter(WeatherStationState.from_date <= date). \
        filter(or_(WeatherStationState.to_date >= date, WeatherStationState.to_date == None)). \
        order_by('dist').first()
    app.json_encoder = WeatherStation.JSONEncoder
    txt = jsonify(station_with_distance[0])
    UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
               auth.current_user()).record_access(db)
    return txt, 200

