import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/home/gisfire/soft/api/lightinings/meteocat/')
from lightnings import app as application
application.secret_key = 'key'
