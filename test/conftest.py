#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pytest_postgresql import factories
from pathlib import Path
import gisfire_meteocat_lib.database
import tempfile


test_folder = Path(__file__).parent
sql_meteocat_lib_folder = Path(gisfire_meteocat_lib.database.__file__).parent
socket_dir = tempfile.TemporaryDirectory()
postgresql_session = factories.postgresql_proc(port=None, unixsocketdir=socket_dir.name)
postgresql_schema = factories.postgresql('postgresql_session', dbname='test', load=[
    str(test_folder) + '/database_init.sql',
    str(test_folder.parent) + '/src/gisfire_api/user/user.sql',
    str(sql_meteocat_lib_folder) + '/meteocat_xdde.sql',
    str(test_folder) + '/database_populate.sql'])

pytest_plugins = ['test.fixtures.api', 'test.fixtures.lightnings']


