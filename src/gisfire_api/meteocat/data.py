#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import jsonify
from flask import request
from flask import current_app as app
from .. import db
from ..auth import auth
from ..user import UserAccess
from gisfire_meteocat_lib.classes.variable import Variable
from gisfire_meteocat_lib.classes.measure import Measure
from sqlalchemy import desc
from sqlalchemy import func
from sqlalchemy import or_
import json
import datetime
import dateutil.parser

from typing import List

bp = Blueprint("meteocat_data", __name__, url_prefix="/v1/meteocat/data")


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


@bp.route('/measure/<station>/<variable>/', methods=['GET'])
@bp.route('/measure/<station>/<variable>', methods=['GET'])
@auth.login_required(role='user')
def get_measure_of_variable_at_station(station: str, variable: str):
    """
    TODO:

    :return:
    :rtype:
    """
    # Check we have basic parameters
    if (request.values is None) or ('date' not in request.values) or (not (1 <= len(request.values) <= 2)):
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
    if 'operation' in request.values:
        operation_data = request.values['operation'].split(',')
        if (operation_data[0] == 'average') and (len(operation_data) == 2):
            operation = 'average'
            try:
                days = int(operation_data[1])
            except ValueError as _:
                UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                           auth.current_user()).record_access(db, 400)
        else:
            UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                       auth.current_user()).record_access(db, 400)
            return jsonify(status_code=400), 400
    else:
        operation = 'value'
    # TODO: Check the station is active for the current date
    # TODO: Check the variable is valid for the station in the current date
    if operation == 'value':
        # TODO: Retrieve the measure
        measure: Measure = db.session.query(Measure).\
            filter(Measure.date <= date).\
            order_by(desc(Measure.date)).first()
        if measure is None:
            pass
        app.json_encoder = Measure.JSONEncoder
        txt = jsonify(measure)
        UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                   auth.current_user()).record_access(db)
        return txt, 200
    elif operation == 'average':
        txt = jsonify({})
        UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                   auth.current_user()).record_access(db)
        return txt, 200

