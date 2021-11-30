#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from src.gisfire_api import create_app


@pytest.fixture
def api(postgresql_schema):
    cursor = postgresql_schema.cursor()
    cursor.execute("SET SESSION AUTHORIZATION gisfireuser; SET ROLE gisfireuser;")
    postgresql_schema.commit()

    app = create_app(postgresql_schema)
    app.config['TESTING'] = True
    app.config['DEBUG'] = True

    with app.test_client() as client:
        yield client

