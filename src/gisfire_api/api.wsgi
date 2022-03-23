import logging
import sys
import os
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/home/gisfire/soft/GisFIRE-API/src/')

params = dict()
params['GISFIRE_DB_HOST'] = os.environ['GISFIRE_DB_HOST']
params['GISFIRE_DB_PORT'] = os.environ['GISFIRE_DB_PORT']
params['GISFIRE_DB_DATABASE'] = os.environ['GISFIRE_DB_DATABASE']
params['GISFIRE_DB_USERNAME'] = os.environ['GISFIRE_DB_USERNAME']
params['GISFIRE_DB_PASSWORD'] = os.environ['GISFIRE_DB_PASSWORD']

from gisfire_api import create_app
application = create_app(params=params)
application.secret_key = '12345678998765431'
