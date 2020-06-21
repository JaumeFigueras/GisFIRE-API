import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/home/gisfire/soft/GisFIRE-API/tokens/')
from tokens import app as application
application.secret_key = 'key'
