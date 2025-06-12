import pytest

def test_management_access_without_login(client):
    # Attempt to access management without logging in
    resp = client.get("/management/")
    assert resp.status_code == 302, "Should redirect to login"
    assert resp.headers['Location'].endswith('/auth/login'), "Should redirect to login page"
    
@pytest.mark.usefixtures("login_as_admin")
def test_add_asset_and_delete(client):
    # Add
    asset_data = {
        "Name": "PyTestAsset",
        "Type": "Electronics",
        "Status": "Unassigned"
    }
    add_resp = client.post("/management/add-record/asset", json=asset_data)
    assert add_resp.status_code == 201
    assert "added successfully" in add_resp.get_json()["message"]