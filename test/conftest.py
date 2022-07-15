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
# TODO: Load different schemas depending on tests to do to optimize time
postgresql_auth_schema = factories.postgresql('postgresql_session', dbname='test_auth', load=[
    str(test_folder) + '/database_init.sql',
    str(test_folder.parent) + '/src/gisfire_api/user/user.sql',
    str(sql_meteocat_lib_folder) + '/meteocat_xdde.sql',
    str(sql_meteocat_lib_folder) + '/meteocat_xema.sql',
    str(test_folder) + '/sql-data/database_populate.sql',
    ]
)
postgresql_schema = factories.postgresql('postgresql_session', dbname='test', load=[
    str(test_folder) + '/database_init.sql',
    str(test_folder.parent) + '/src/gisfire_api/user/user.sql',
    str(sql_meteocat_lib_folder) + '/meteocat_xdde.sql',
    str(sql_meteocat_lib_folder) + '/meteocat_xema.sql',
    str(test_folder) + '/sql-data/lightnings.sql',
    str(test_folder) + '/sql-data/database_populate.sql',
    str(test_folder) + '/sql-data/stations-11st.sql',
    str(test_folder) + '/sql-data/stations-states-11st.sql',
    str(test_folder) + '/sql-data/variables.sql',
    str(test_folder) + '/sql-data/variables-states.sql',
    str(test_folder) + '/sql-data/variables-timebases.sql',
    str(test_folder) + '/sql-data/stations-variables-states-11st.sql',
    str(test_folder) + '/sql-data/stations-variables-timebases-11st.sql',
    str(test_folder) + '/sql-data/measures-11st.sql',
    str(test_folder) + '/sql-data/land-cover-schema.sql',
    str(test_folder) + '/sql-data/land-cover.sql',
    ]
)

pytest_plugins = ['test.fixtures.api', 'test.fixtures.lightnings']

"""
Stations used

(141, 33, 76, 50, 232, 146, 96, 164, 47, 202, 117)

"""

