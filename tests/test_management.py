import pytest
import re

def find_id_by_field(html, field_value):
    """
    Finds the ID (first <td>) in the row where any cell matches field_value.
    """
    # Find all rows
    rows = re.findall(r'<tr.*?>(.*?)</tr>', html, re.DOTALL)
    for row in rows:
        if field_value in row:
            # Find the first <td> number in the row
            match = re.search(r'<td.*?>(\d+)</td>', row)
            if match:
                return int(match.group(1))
    return None

def test_management_access_without_login(client):
    # Attempt to access management without logging in
    resp = client.get("/management/")
    assert resp.status_code == 302, "Should redirect to login"
    assert resp.headers['Location'].endswith('/auth/login'), "Should redirect to login page"

@pytest.mark.usefixtures("login_as_user")
def test_management_access_as_user(client):
    # Regular user should NOT see management page
    resp = client.get("/management/")
    # Should be redirected to login or get 403, depending on your logic
    assert resp.status_code in (302, 403)
    
@pytest.mark.usefixtures("login_as_admin")
def test_asset_crud(client):
    # Add asset
    asset_data = {"Name": "PyTestAsset", "Type": "Electronics", "Status": "Unassigned"}
    add_resp = client.post("/management/add-record/asset", json=asset_data)
    assert add_resp.status_code == 201

    # Find asset_id in management table
    mgmt_html = client.get("/management/").data.decode()
    asset_id = find_id_by_field(mgmt_html, "PyTestAsset")
    assert asset_id is not None

    # Edit asset
    updated = {"AssetID": asset_id, "Name": "PyTestAsset-Edit", "Type": "Electronics", "Status": "Assigned"}
    edit = client.post(f"/management/update-record/asset/{asset_id}", json=updated)
    assert edit.status_code == 200

    # Confirm edit
    asset = client.get(f"/management/get-record/asset/{asset_id}").get_json()
    assert asset["Name"] == "PyTestAsset-Edit"
    assert asset["Status"] == "Assigned"

    # Delete asset
    del_resp = client.post(f"/management/delete-record/asset/{asset_id}")
    assert del_resp.status_code == 200

    # Confirm delete
    get_deleted = client.get(f"/management/get-record/asset/{asset_id}")
    assert get_deleted.status_code == 404

@pytest.mark.usefixtures("login_as_admin")
def test_user_crud(client):
    # Add user
    user_data = {
        "Forename": "PyTest",
        "Surname": "User",
        "Username": "pytestuser",
        "Password": "Password1234",
        "Role": "Regular"
    }
    
    
    add_user = client.post("/management/add-record/user", json=user_data)
    assert add_user.status_code == 201

    # Find user_id
    mgmt_html = client.get("/management/").data.decode()
    user_id = find_id_by_field(mgmt_html, "pytestuser")
    assert user_id is not None
    print("DEBUG: user_id =", user_id)

    # Edit user
    updated_user = {
        "UserID": user_id,
        "Forename": "PyTestEdit",
        "Surname": "UserEdit",
        "Username": "pytestuser",
        "Password": "Password1234",
        "Role": "Regular"
    }
    edit = client.post(f"/management/update-record/user/{user_id}", json=updated_user)
    assert edit.status_code == 200

    # Confirm edit
    user = client.get(f"/management/get-record/user/{user_id}").get_json()
    assert user["Forename"] == "PyTestEdit"
    assert user["Surname"] == "UserEdit"

    # Delete user
    del_resp = client.post(f"/management/delete-record/user/{user_id}")
    assert del_resp.status_code == 200

    # Confirm delete
    get_deleted = client.get(f"/management/get-record/user/{user_id}")
    assert get_deleted.status_code == 404
    
@pytest.mark.usefixtures("login_as_admin")
def test_loan_crud(client):
    # Use IDs that exist (adjust as needed for your seed data)
    asset_id = 7   # Unassigned asset in seed
    user_id = 3    # Existing user in seed

    # Add loan
    loan_data = {
        "AssetID": asset_id,
        "UserID": user_id,
        "LoanDate": "2025-06-01",
        "ReturnDate": None
    }
    add_loan = client.post("/management/add-record/loan", json=loan_data)
    assert add_loan.status_code == 201

    # Find loan_id
    mgmt_html = client.get("/management/").data.decode()
    loan_id = find_id_by_field(mgmt_html, "2025-06-01")  # crude, better to match on all fields if possible
    assert loan_id is not None

    # Edit loan
    updated_loan = {
        "LoanID": loan_id,
        "AssetID": asset_id,
        "UserID": user_id,
        "LoanDate": "2025-06-01",
        "ReturnDate": "2025-06-10"
    }
    edit = client.post(f"/management/update-record/loan/{loan_id}", json=updated_loan)
    assert edit.status_code == 200

    # Confirm edit
    loan = client.get(f"/management/get-record/loan/{loan_id}").get_json()
    assert loan["ReturnDate"] == "2025-06-10"

    # Delete loan
    del_resp = client.post(f"/management/delete-record/loan/{loan_id}")
    assert del_resp.status_code == 200

    # Confirm delete
    get_deleted = client.get(f"/management/get-record/loan/{loan_id}")
    assert get_deleted.status_code == 404