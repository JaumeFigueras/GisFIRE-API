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

import json
import pytz
import datetime

bp = Blueprint("meteocat_lightning", __name__, url_prefix="/v1/meteocat/lightning")


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
    if is_today:
        hours = today.hour
    else:
        hours = 24
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
            # Get the token to query MeteoCat API
            token = request.headers.get('X-Api-Key', '')
            if token == '':
                UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                           auth.current_user()).record_access(db, 401)
                return jsonify(status_code=401), 401
            # Request MeteoCat API
            result = meteocat_xdde_api.get_lightnings(token, date.date(), hour)
            if not (result['status_code'] is None):
                # There is a response
                if result['status_code'] != 200:
                    # The response is not successful, so the error is recorded and passed
                    light_request = LightningAPIRequest(current_date, result['status_code'])
                    db.session.add(light_request)
                    UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                               auth.current_user()).record_access(db, result['status_code'])
                    return (jsonify({'status_code': result['status_code'], 'message': result['message']}),
                            result['status_code'])
                # The response is successful, the data and access are recorded and added to the lightnings list and
                # continue loop
                light_request = LightningAPIRequest(current_date, result['status_code'], len(result['data']))
                db.session.add(light_request)
                if len(result['data']) > 0:
                    db.session.add(result['data'])
                lightnings += result['data']
            else:
                # There is no response, so an exception should have occurred
                UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                           auth.current_user()).record_access(db, 500)
                return jsonify(status_code=500), 500
        else:
            # The date has been requested before
            if req.http_status_code == 200:
                # It has been requested successfully
                if req.number_of_lightnings != 0:
                    # There are lightnings to process
                    lights = db.session.query(Lightning). \
                        filter(Lightning.date >= current_date). \
                        filter(Lightning.date < current_date + datetime.timedelta(hours=1)). \
                        all()
                    # TODO: Add order by
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
                # TODO: Refactor to extract function and pass the request database object to update it
                pass
    app.json_encoder = Lightning.JSONEncoder
    UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
               auth.current_user()).record_access(db)
    return jsonify(lightnings), 200
