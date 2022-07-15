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
from gisfire_meteocat_lib.classes.variable import Variable
from gisfire_meteocat_lib.classes.variable import VariableState
from gisfire_meteocat_lib.classes.variable import VariableStateCategory
from gisfire_meteocat_lib.classes.relations import WeatherStationVariableStateAssociation
from gisfire_meteocat_lib.classes.measure import Measure
from gisfire_meteocat_lib.classes.measure import MeasureValidityCategory
from gisfire_meteocat_lib.classes.measure import MeasureTimeBaseCategory
from sqlalchemy import desc
from sqlalchemy import func
from sqlalchemy import or_
import json
import datetime
import dateutil.parser
from typing import Union

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


@bp.route('/measure/<station_code>/<variable_code>/', methods=['GET'])
@bp.route('/measure/<station_code>/<variable_code>', methods=['GET'])
@auth.login_required(role='user')
def get_measure_of_variable_at_station(station_code: str, variable_code: str):
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
    days = 0
    if 'operation' in request.values:
        operation_data = request.values['operation'].split(',')
        if (operation_data[0] == 'average') and (len(operation_data) == 2):
            operation = 'average'
            try:
                days = int(operation_data[1])
                if days < 1:
                    UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                               auth.current_user()).record_access(db, 400)
                    return jsonify(status_code=400), 400
            except ValueError as _:
                UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                           auth.current_user()).record_access(db, 400)
                return jsonify(status_code=400), 400
        elif (operation_data[0] == 'sum') and (len(operation_data) == 2):
            operation = 'sum'
            try:
                days = int(operation_data[1])
                if days < 1:
                    UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                               auth.current_user()).record_access(db, 400)
                    return jsonify(status_code=400), 400
            except ValueError as _:
                UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                           auth.current_user()).record_access(db, 400)
                return jsonify(status_code=400), 400
        elif (operation_data[0] == 'max') and (len(operation_data) == 2):
            operation = 'max'
            try:
                days = int(operation_data[1])
                if days < 1:
                    UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                               auth.current_user()).record_access(db, 400)
                    return jsonify(status_code=400), 400
            except ValueError as _:
                UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                           auth.current_user()).record_access(db, 400)
                return jsonify(status_code=400), 400
        else:
            UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                       auth.current_user()).record_access(db, 400)
            return jsonify(status_code=400), 400
    else:
        operation = 'value'
    # Check the station is active for the current date
    station: WeatherStation = db.session.query(WeatherStation). \
        join(WeatherStationState, WeatherStation.id == WeatherStationState.meteocat_weather_station_id). \
        filter(WeatherStation.code == station_code). \
        filter(WeatherStationState.code == WeatherStationStateCategory.ACTIVE). \
        filter(WeatherStationState.from_date <= date). \
        filter(or_(WeatherStationState.to_date >= date, WeatherStationState.to_date == None)). \
        first()
    if station is None:
        UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                   auth.current_user()).record_access(db, 400)
        return jsonify({"status_code": 400, "reason": "Station not active in provided date"}), 400
    # Check the variable is valid for the station in the current date
    variable: Variable = db.session.query(Variable). \
        join(WeatherStationVariableStateAssociation, Variable.id == WeatherStationVariableStateAssociation.meteocat_variable_id). \
        join(WeatherStation, WeatherStation.id == WeatherStationVariableStateAssociation.meteocat_weather_station_id). \
        join(VariableState, VariableState.id == WeatherStationVariableStateAssociation.meteocat_variable_state_id). \
        filter(WeatherStation.id == station.id). \
        filter(Variable.acronym == variable_code). \
        filter(VariableState.code == VariableStateCategory.ACTIVE). \
        filter(VariableState.from_date <= date). \
        filter(or_(VariableState.to_date >= date, VariableState.to_date == None)). \
        first()
    if variable is None:
        UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                   auth.current_user()).record_access(db, 400)
        return jsonify({"status_code": 400, "reason": "Variable not active in provided date for selected station"}), 400
    if operation == 'value':
        # Retrieve the measure
        measure: Measure = db.session.query(Measure). \
            filter(Measure.date <= date). \
            filter(Measure.meteocat_weather_station_id == station.id). \
            filter(Measure.meteocat_variable_id == variable.id). \
            order_by(desc(Measure.date)).first()
        if measure is None:
            UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                       auth.current_user()).record_access(db, 400)
            return jsonify({"status_code": 400, "reason": "Measure not found"}), 400
        else:
            # TODO: Check time depending on variable time base
            max_distance: int = 30 * 60  # Seconds in a SH (30 min) measure and variable
            delta: datetime.timedelta = date - measure.date
            if (delta.days > 0) or (delta.seconds >= max_distance):
                UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                           auth.current_user()).record_access(db, 400)
                return jsonify({"status_code": 400, "reason": "Measure date found"}), 400
        app.json_encoder = Measure.JSONEncoder
        txt = jsonify(measure)
        UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                   auth.current_user()).record_access(db)
        return txt, 200
    elif operation == 'average':
        # Retrieve the measure
        date_to = date
        date_from = date - datetime.timedelta(days=days)
        average: List[Union[float, None]] = db.session.query(func.avg(Measure.value)). \
            filter(Measure.date <= date_to). \
            filter(Measure.date >= date_from). \
            filter(Measure.meteocat_weather_station_id == station.id). \
            filter(Measure.meteocat_variable_id == variable.id).first()
        if average[0] is None:
            UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                       auth.current_user()).record_access(db, 400)
            return jsonify({"status_code": 400, "reason": "Average can't be calculated"}), 400
        app.json_encoder = Measure.JSONEncoder
        measure: Measure = Measure(date=date, date_extreme=None, value=average[0],
                                   validity_state=MeasureValidityCategory.VALID, time_base=MeasureTimeBaseCategory.SH)
        txt = jsonify(measure)
        UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                   auth.current_user()).record_access(db)
        return txt, 200
    elif operation == 'sum':
        # Retrieve the measure
        date_to = date
        date_from = date - datetime.timedelta(days=days)
        sum: List[Union[float, None]] = db.session.query(func.sum(Measure.value)). \
            filter(Measure.date <= date_to). \
            filter(Measure.date >= date_from). \
            filter(Measure.meteocat_weather_station_id == station.id). \
            filter(Measure.meteocat_variable_id == variable.id).first()
        if sum[0] is None:
            UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                       auth.current_user()).record_access(db, 400)
            return jsonify({"status_code": 400, "reason": "Average can't be calculated"}), 400
        app.json_encoder = Measure.JSONEncoder
        measure: Measure = Measure(date=date, date_extreme=None, value=sum[0],
                                   validity_state=MeasureValidityCategory.VALID, time_base=MeasureTimeBaseCategory.SH)
        txt = jsonify(measure)
        UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                   auth.current_user()).record_access(db)
        return txt, 200
    elif operation == 'max':
        # Retrieve the measure
        date_to = date
        date_from = date - datetime.timedelta(days=days)
        sum: List[Union[float, None]] = db.session.query(func.max(Measure.value)). \
            filter(Measure.date <= date_to). \
            filter(Measure.date >= date_from). \
            filter(Measure.meteocat_weather_station_id == station.id). \
            filter(Measure.meteocat_variable_id == variable.id).first()
        if sum[0] is None:
            UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                       auth.current_user()).record_access(db, 400)
            return jsonify({"status_code": 400, "reason": "Average can't be calculated"}), 400
        app.json_encoder = Measure.JSONEncoder
        measure: Measure = Measure(date=date, date_extreme=None, value=sum[0],
                                   validity_state=MeasureValidityCategory.VALID, time_base=MeasureTimeBaseCategory.SH)
        txt = jsonify(measure)
        UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                   auth.current_user()).record_access(db)
        return txt, 200


