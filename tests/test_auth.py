import pytest

def test_signup_and_login(client):
    """
    1) POST to /auth/signup with valid data → expect 200 and JSON message.
    2) Then POST to /auth/login with the same credentials → expect login success.
    """

    # 1. Sign up a new user
    signup_payload = {
        "forename": "Alice",
        "surname": "Test",
        "username": "alice123",
        "password": "Passw0rd" 
    }
    signup_resp = client.post(
        "/auth/signup",
        json=signup_payload
    )
    assert signup_resp.status_code == 200, "Signup should return 200"
    signup_data = signup_resp.get_json()
    assert signup_data["message"] == "Signup successful"

    # 2. Log out (in case session is still set) then login as Alice
    # Note: your logout endpoint is @auth_bp.route('logout'), missing a leading slash.
    # If it's actually "/auth/logout", adjust accordingly. Here we'll assume "/auth/logout":
    client.get("/auth/logout")

    login_payload = {
        "username": "alice123",
        "password": "Passw0rd"
    }
    login_resp = client.post(
        "/auth/login",
        json=login_payload
    )
    assert login_resp.status_code == 200, "Login should return 200"
    login_data = login_resp.get_json()
    assert login_data["message"] == "Login successful"
    assert "redirect" in login_data and login_data["redirect"] == "/home"

def test_signup_password_validation(client):
    bad_payload = {
        "forename": "Bob",
        "surname": "Test",
        "username": "bob123",
        "password": "short"
    }
    resp = client.post("/auth/signup", json=bad_payload)
    assert resp.status_code == 400
    data = resp.get_json()
    assert "Password must be at least 8 characters" in data["message"]


def test_login_invalid_credentials(client):
    payload = {
        "username": "doesnotexist",
        "password": "whatever123"
    }
    resp = client.post("/auth/login", json=payload)
    assert resp.status_code == 401
    data = resp.get_json()
    assert data["message"] == "Invalid credentials"
