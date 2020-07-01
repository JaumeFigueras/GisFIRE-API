import pytest
import testing.postgresql

from lightnings.meteocat import lightnings

@pytest.fixture
def client():
    lightnings.app.config['TESTING'] = True

    with lightnings.app.test_client() as client:
        yield client

def test_empty_db(client):
    """Start with a blank database."""

    rv = client.get('/')
    assert b'No entries here so far' in rv.data
