def test_get_current_user_returns_authenticated_manager(client):
    registration_response = client.post(
        "/api/auth/register",
        json={
            "business_name": "ASI Kitchen",
            "email": "owner@example.com",
            "password": "StrongPass123!",
        },
    )
    registered_user = registration_response.json()

    login_response = client.post(
        "/api/auth/login",
        json={
            "email": "owner@example.com",
            "password": "StrongPass123!",
        },
    )
    access_token = login_response.json()["access_token"]

    response = client.get(
        "/api/auth/me",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["id"] == registered_user["id"]
    assert response_data["business_name"] == "ASI Kitchen"
    assert response_data["email"] == "owner@example.com"
    assert "password_hash" not in response_data


def test_get_current_user_requires_access_token(client):
    response = client.get("/api/auth/me")

    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials."}


def test_get_current_user_rejects_invalid_access_token(client):
    response = client.get(
        "/api/auth/me",
        headers={
            "Authorization": "Bearer not-a-valid-token",
        },
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials."}
