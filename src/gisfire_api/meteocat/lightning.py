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
from geoalchemy2.types import Geometry
import json
import pytz
import datetime

from typing import List
from typing import Tuple

bp = Blueprint("meteocat_lightning", __name__, url_prefix="/v1/meteocat/lightning")


# Create the land cover private class
class LandCover(db.Model):
    __tablename__ = 'data_catalonia_land_cover'
    __table_args__ = {'extend_existing': True}
    fid = db.Column('fid', db.Integer, primary_key=True)
    id = db.Column('id', db.Integer)
    nivell_2 = db.Column('nivell_2', db.Integer)
    geom = db.Column('geom', Geometry(geometry_type='POLYGON', srid=25831))


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


@bp.route('/<int:year>/<int:month>/<int:day>/', methods=['GET'])
@bp.route('/<int:year>/<int:month>/<int:day>', methods=['GET'])
@auth.login_required(role='user')
def get_lightnings(year, month, day):
    """
    TODO:

    :param year:
    :param month:
    :param day:
    :return:
    """

    # Check if the requested date is valid
    try:
        date = datetime.datetime(year, month, day, 0, 0, 0, tzinfo=pytz.UTC)
    except ValueError:
        UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                   auth.current_user()).record_access(db, 422)
        return jsonify(status_code=422), 422
    # If the requested date is today, then only the previous hour can be requested, if not, then the whole day can be
    # requested
    today = datetime.datetime.utcnow()
    is_today = date.date() == today.date()
    if today.date() < date.date():
        UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                   auth.current_user()).record_access(db, 400)
        return jsonify(status_code=400), 400
    if is_today:
        if today.hour == 0:
            hours = 0
        else:
            hours = today.hour  # Should be hour - 1, but then the range must be hour + 1. So hour is OK
    else:
        hours = 24
    # Get the possible output SRID
    srid = request.args.get('srid', default=None, type=int)
    # Get the possible output format
    output_format = request.args.get('format', default='json', type=str)
    # For all the possible hours to request
    lightnings = list()
    for hour in range(hours):
        # Add the hour to the date
        current_date = datetime.datetime(date.year, date.month, date.day, hour, 0, 0, tzinfo=pytz.UTC)
        # Check if it has been asked before
        req = db.session.query(LightningAPIRequest). \
            filter(LightningAPIRequest.date == current_date). \
            first()
        if req is None:
            # There are no previous requests recorded
            # Make a query to the MeteoCat API
            lightnings, status_code = get_from_remote(current_date, lightnings)
        else:
            # The date has been requested before
            status_code = 200
            if req.http_status_code == 200:
                # It has been requested successfully
                if req.number_of_lightnings != 0:
                    # There are lightnings to process
                    if srid is None:
                        lights = db.session.query(Lightning). \
                            filter(Lightning.date >= current_date). \
                            filter(Lightning.date < current_date + datetime.timedelta(hours=1)). \
                            order_by(Lightning.date). \
                            all()
                    else:
                        mixed = db.session.query(Lightning, func.ST_X(Lightning.geometry.ST_Transform(int(srid))),
                                                 func.ST_Y(Lightning.geometry.ST_Transform(int(srid)))). \
                            filter(Lightning.date >= current_date). \
                            filter(Lightning.date < current_date + datetime.timedelta(hours=1)). \
                            order_by(Lightning.date). \
                            all()
                        lights = list()
                        for lightning, x, y in mixed:
                            lightning.y = y
                            lightning.x = x
                            lightning.srid = srid
                            lights.append(lightning)
                    if len(lights) != req.number_of_lightnings:
                        # A problem with the database have appeared
                        UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                                   auth.current_user()).record_access(db, 500)
                        return jsonify(status_code=500), 500
                    else:
                        # The lightnings are added to the list
                        lightnings += lights
            else:
                # The previous request was unsuccessful
                # Make a query to the MeteoCat API
                lightnings, status_code = get_from_remote(current_date, lightnings)
        if status_code != 200:
            return jsonify(status_code=status_code), status_code
    if output_format == 'json':
        app.json_encoder = Lightning.JSONEncoder
    elif output_format == 'geojson':
        app.json_encoder = Lightning.GeoJSONEncoder
    else:
        app.json_encoder = Lightning.JSONEncoder
    txt = jsonify(lightnings)
    UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
               auth.current_user()).record_access(db)
    return txt, 200


def get_from_remote(current_date: datetime.datetime, lightnings: List[Lightning]) -> Tuple[List[Lightning], int]:
    """
    TODO:

    :param current_date:
    :param lightnings:
    :return:
    """
    # Get the MeteoCap API access token
    token = request.headers.get('X-Api-Key', '')
    if token == '':
        UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                   auth.current_user()).record_access(db, 401)
        return lightnings, 401
    # Request MeteoCat API
    try:
        result = meteocat_xdde_api.get_lightnings(token, current_date)
        new_lightnings: List[Lightning] = result['lightnings']
        lightning_request: LightningAPIRequest = result['lightning_api_request']
        if not (lightning_request.http_status_code is None):
            # There is a response
            if lightning_request.http_status_code != 200:
                # The response is not successful, so the error is recorded and passed
                light_request = db.session.query(LightningAPIRequest).\
                    filter(LightningAPIRequest.date == current_date).\
                    first()
                if light_request is None:
                    light_request = LightningAPIRequest(current_date, lightning_request.http_status_code)
                    db.session.add(light_request)
                else:
                    light_request.http_status_code = lightning_request.http_status_code
                    db.session.commit()
                UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                           auth.current_user()).record_access(db, lightning_request.http_status_code)
                return lightnings, lightning_request.http_status_code
            else:
                # The response is successful, the data and access are recorded and added to the lightnings list and
                # continue loop
                light_request = db.session.query(LightningAPIRequest).\
                    filter(LightningAPIRequest.date == current_date).\
                    first()
                if light_request is None:
                    light_request = LightningAPIRequest(current_date, lightning_request.http_status_code,
                                                        lightning_request.number_of_lightnings)
                    db.session.add(light_request)
                else:
                    light_request.http_status_code = lightning_request.http_status_code
                    light_request.number_of_lightnings = lightning_request.number_of_lightnings
                    db.session.commit()
                if lightning_request.number_of_lightnings > 0:
                    db.session.bulk_save_objects(new_lightnings)
                lightnings += new_lightnings
                return lightnings, 200
        else:
            # There is no response, so an exception should have occurred
            UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                       auth.current_user()).record_access(db, 500)
            return lightnings, 500
    except RequestException:
        # There is no response, so an exception should have occurred
        UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                   auth.current_user()).record_access(db, 500)
        return lightnings, 500


@bp.route('/<int:identifier>/', methods=['GET'])
@bp.route('/<int:identifier>', methods=['GET'])
@auth.login_required(role='user')
def get_lightning(identifier):
    """
    TODO:

    :param identifier:
    :return:
    """
    srid: int = Lightning.DEFAULT_SRID_LIGHTNINGS
    hours: int = 6
    if request.values is not None:
        if 'srid' in request.values:
            srid: str = request.values['srid']
            try:
                srid: int = int(srid)
            except ValueError as _:
                UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                           auth.current_user()).record_access(db, 400)
                return jsonify(status_code=400), 400
    if srid == Lightning.DEFAULT_SRID_LIGHTNINGS:
        lightning = db.session.query(Lightning).filter(Lightning.id == identifier).first()
    else:
        lightning, x, y = db.session.query(Lightning, func.ST_X(Lightning.geometry.ST_Transform(srid)),
                                           func.ST_Y(Lightning.geometry.ST_Transform(srid))). \
            filter(Lightning.id == identifier).first()
        if lightning is not None:
            lightning.y = y
            lightning.x = x
            lightning.srid = srid
    if lightning is None:
        UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                   auth.current_user()).record_access(db, 404)
        return jsonify(status_code=404), 404
    app.json_encoder = Lightning.JSONEncoder
    txt = jsonify(lightning)
    UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
               auth.current_user()).record_access(db)
    return txt, 200


@bp.route('/near/<int:identifier>/<distance>/', methods=['GET'])
@bp.route('/near/<int:identifier>/<distance>', methods=['GET'])
@auth.login_required(role='user')
def get_near_lightnings(identifier: int, distance: float):
    """
    TODO:

    :return:
    :rtype:
    """
    srid: int = Lightning.DEFAULT_SRID_LIGHTNINGS
    hours: int = 6
    if request.values is not None:
        if 'srid' in request.values:
            srid: str = request.values['srid']
            try:
                srid: int = int(srid)
            except ValueError as _:
                UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                           auth.current_user()).record_access(db, 400)
                return jsonify(status_code=400), 400
    # Convert distance to float
    try:
        distance: float = float(distance)
    except ValueError as _:
        UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                   auth.current_user()).record_access(db, 400)
        return jsonify(status_code=400), 400

    # Check the lightning exists
    lightning, x, y = db.session.query(Lightning, func.ST_X(Lightning.geometry.ST_Transform(srid)),
                                       func.ST_Y(Lightning.geometry.ST_Transform(srid))).\
        filter(Lightning.id == identifier).first()
    if lightning is None:
        UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                   auth.current_user()).record_access(db, 404)
        return jsonify(status_code=404), 404
    lightning.y = y
    lightning.x = x
    lightning.srid = srid
    lightnings = db.session.query(Lightning).\
        filter(func.ST_Contains(func.ST_Buffer(func.ST_GeomFromEWKT('SRID={0:d};POINT({1:f} {2:f})'.format(srid, x, y)), distance), func.ST_Transform(Lightning.geometry, srid))).\
        filter(Lightning.date <= lightning.date).\
        filter(Lightning.date >= lightning.date - datetime.timedelta(hours=6)).\
        filter(Lightning.id != identifier).\
        all()
    if lightning is None:
        UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                   auth.current_user()).record_access(db)
        return jsonify([]), 200
    else:
        app.json_encoder = Lightning.JSONEncoder
        txt = jsonify(lightnings)
        UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                   auth.current_user()).record_access(db)
        return txt, 200


@bp.route('/land_cover/<int:identifier>/', methods=['GET'])
@bp.route('/land_cover/<int:identifier>', methods=['GET'])
@auth.login_required(role='user')
def get_lightning_land_cover(identifier: int):
    """
    TODO:

    :return:
    :rtype:
    """

    # Check the lightning exists
    lightning = db.session.query(Lightning).filter(Lightning.id == identifier).first()
    if lightning is None:
        UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                   auth.current_user()).record_access(db, 404)
        return jsonify(status_code=404), 404
    land_cover = db.session.query(LandCover).\
        filter(func.ST_Contains(LandCover.geom, func.ST_Transform(lightning.geometry, 25831))).\
        first()
    if land_cover is not None:
        txt = jsonify(land_cover_type=land_cover.nivell_2)
    else:
        txt = jsonify(land_cover_type=0)
    UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
               auth.current_user()).record_access(db)
    return txt, 200


@bp.route('/discharge_count/<int:identifier>/', methods=['GET'])
@bp.route('/discharge_count/<int:identifier>', methods=['GET'])
@auth.login_required(role='user')
def get_lightning_discharge_count(identifier: int):
    """
    TODO:

    :return:
    :rtype:
    """

    # Check the lightning exists
    lightning = db.session.query(Lightning).filter(Lightning.id == identifier).first()
    if lightning is None:
        UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                   auth.current_user()).record_access(db, 404)
        return jsonify(status_code=404), 404
    count = db.session.query(func.count(Lightning.meteocat_id)).\
        filter(Lightning.meteocat_id == lightning.meteocat_id).\
        first()
    if count is not None:
        txt = jsonify(count=count[0])
    else:
        txt = jsonify(count=1)
    UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
               auth.current_user()).record_access(db)
    return txt, 200


@bp.route('/grouped_by_discharges/<int:year>/<int:month>/<int:day>/', methods=['GET'])
@bp.route('/grouped_by_discharges/<int:year>/<int:month>/<int:day>', methods=['GET'])
@auth.login_required(role='user')
def get_lightnings_group_by(year, month, day):
    """
    TODO:

    :param year:
    :param month:
    :param day:
    :return:
    """

    # Check if the requested date is valid
    try:
        date = datetime.datetime(year, month, day, 0, 0, 0, tzinfo=pytz.UTC)
    except ValueError:
        UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                   auth.current_user()).record_access(db, 422)
        return jsonify(status_code=422), 422
    srid = Lightning.DEFAULT_SRID_LIGHTNINGS
    if request.values is not None:
        if 'srid' in request.values:
            srid: str = request.values['srid']
            try:
                srid: int = int(srid)
            except ValueError as _:
                UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                           auth.current_user()).record_access(db, 400)
                return jsonify(status_code=400), 400
    lightnings = db.session.query(func.min(Lightning.id), Lightning.meteocat_id, func.min(Lightning.date),
                                  func.count(Lightning.id),
                                  func.min(Lightning.peak_current), func.max(Lightning.peak_current),
                                  func.avg(Lightning.chi_squared), func.max(Lightning.number_of_sensors),
                                  func.avg(func.ST_X(Lightning.geometry.ST_Transform(srid))),
                                  func.avg(func.ST_Y(Lightning.geometry.ST_Transform(srid)))).\
        filter(Lightning.date >= date).\
        filter(Lightning.date < (date + datetime.timedelta(days=1))).\
        group_by(Lightning.meteocat_id).\
        order_by(Lightning.meteocat_id).\
        all()
    lightning_list = list()
    for lightning in lightnings:
        lightning_list.append({
            'id': lightning[0],
            'meteocat_id': lightning[1],
            'date': lightning[2].strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            'discharges': lightning[3],
            'peak_current_min': lightning[4],
            'peak_current_max': lightning[5],
            'chi_squared': lightning[6],
            'number_of_sensors': lightning[7],
            'x': lightning[8],
            'y': lightning[9]
        })
    txt = jsonify(lightning_list)
    UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
               auth.current_user()).record_access(db)
    return txt, 200


