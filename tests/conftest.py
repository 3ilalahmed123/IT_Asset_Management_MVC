# tests/conftest.py
import os
import sys
import tempfile
import pytest


# Set Project Root to the parent directory of this file
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# Insert that path at the front of sys.path so `import app` works
sys.path.insert(0, PROJECT_ROOT)


from app import app, init_db
import db as db_module 

@pytest.fixture
def client():
    """
    - Creates a temporary SQLite file
    - Overrides db_module.DATABASE so get_db() points to the temp file
    - Calls init_db() (which runs schema.sql) to create all tables
    - Yields Flask’s test_client() so tests can issue requests
    - Deletes the temp file when the test finishes
    """
    # 1) Create a tempfile to act as our database
    db_fd, db_path = tempfile.mkstemp(suffix=".db")

    # 2) Tell code to use this temp file instead of the real data.db
    app.config['TESTING'] = True
    db_module.DATABASE = db_path

    # 3) Initialize the schema in that temp DB
    with app.app_context():
        init_db()

    # 4) Yield a test client
    with app.test_client() as test_client:
        yield test_client

    # 5) Teardown: close & delete the temp file
    os.close(db_fd)
    os.unlink(db_path)
    
    
@pytest.fixture
def login_as_user(client):
    """
    Logs in as 'user1' before the test.
    """
    payload = {"username": "user1", "password": "password123"}
    resp = client.post("/auth/login", json=payload)
    assert resp.status_code == 200
    
    
@pytest.fixture
def login_as_admin(client):
    """
    Logs in as 'admin1' before the test.
    """
    payload = {"username": "admin1", "password": "password123"}
    resp = client.post("/auth/login", json=payload)
    assert resp.status_code == 200
