import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/home/stock/soft/stock-ml/')
from api import create_app
application = create_app()
application.secret_key = 'key'
