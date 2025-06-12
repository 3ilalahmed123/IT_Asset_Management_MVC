import pytest

def test_home_access_without_login(client):
    # Attempt to access home without logging in
    resp = client.get("/home/")
    assert resp.status_code == 302, "Should redirect to login"
    assert resp.headers['Location'].endswith('/auth/login'), "Should redirect to login page"
    
    
@pytest.mark.usefixtures("login_as_user")
def test_home_access_with_login(client):
    resp = client.get("/home/")
    assert resp.status_code == 200
    assert b"my_assets" in resp.data or b"My Assets" in resp.data
    
@pytest.mark.usefixtures("login_as_user")
def test_loan_asset(client):
    # Use an unassigned asset id from data
    asset_id = 6
    resp = client.post("/home/handle-action", json={
        "actionType": "loan",
        "assetId": asset_id
    })
    assert resp.status_code == 200
    assert "completed successfully" in resp.get_json()["message"]

@pytest.mark.usefixtures("login_as_user")
def test_invalid_action_type(client):
    resp = client.post("/home/handle-action", json={
        "actionType": "invalid",
        "assetId": 6
    })
    assert resp.status_code == 400
    assert "Invalid action type" in resp.get_json()["message"]