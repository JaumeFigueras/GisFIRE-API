import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/home/gisfire/soft/GisFIRE-API/src/gisfire_api/')
from . import create_app
application = create_app()
application.secret_key = '12345678998765431'
