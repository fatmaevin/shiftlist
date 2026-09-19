from sqlalchemy import select

from app.models import User
from app.security import decode_access_token, verify_password


def test_register_creates_manager(client, db_session):
    response = client.post(
        "/api/auth/register",
        json={
            "business_name": " ASI Kitchen ",
            "email": " OWNER@Example.com ",
            "password": "StrongPass123!",
        },
    )

    assert response.status_code == 201

    response_data = response.json()

    assert response_data["business_name"] == "ASI Kitchen"
    assert response_data["email"] == "owner@example.com"
    assert "password" not in response_data
    assert "password_hash" not in response_data

    saved_user = db_session.scalar(
        select(User).where(User.email == "owner@example.com")
    )

    assert saved_user is not None
    assert saved_user.password_hash != "StrongPass123!"
    assert verify_password(
        "StrongPass123!",
        saved_user.password_hash,
    )


def test_register_rejects_duplicate_email(client):
    registration = {
        "business_name": "ASI Kitchen",
        "email": "owner@example.com",
        "password": "StrongPass123!",
    }

    first_response = client.post(
        "/api/auth/register",
        json=registration,
    )
    second_response = client.post(
        "/api/auth/register",
        json=registration,
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert second_response.json() == {
        "detail": "An account with this email already exists."
    }


def test_login_returns_access_token_for_valid_credentials(client):
    registration_response = client.post(
        "/api/auth/register",
        json={
            "business_name": "ASI Kitchen",
            "email": "owner@example.com",
            "password": "StrongPass123!",
        },
    )
    registered_user = registration_response.json()

    response = client.post(
        "/api/auth/login",
        json={
            "email": " OWNER@Example.com ",
            "password": "StrongPass123!",
        },
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["token_type"] == "bearer"
    assert (
        str(decode_access_token(response_data["access_token"])) == registered_user["id"]
    )


def test_login_rejects_wrong_password(client):
    client.post(
        "/api/auth/register",
        json={
            "business_name": "ASI Kitchen",
            "email": "owner@example.com",
            "password": "StrongPass123!",
        },
    )

    response = client.post(
        "/api/auth/login",
        json={
            "email": "owner@example.com",
            "password": "WrongPass123!",
        },
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid email or password."}


def test_login_rejects_unknown_email(client):
    response = client.post(
        "/api/auth/login",
        json={
            "email": "unknown@example.com",
            "password": "StrongPass123!",
        },
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid email or password."}
