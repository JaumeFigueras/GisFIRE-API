import pytest

import lightnings

@pytest.fixture
def client():
    lighnings.app.config['TESTING'] = True

    with lighnings.app.test_client() as client:
        with lighnings.app.app_context():
            pass
        yield client

def test_empty_db(client):
    """Start with a blank database."""

    rv = client.get('/')
    assert b'No entries here so far' in rv.data
