from sqlalchemy import select

from app.models import User
from app.security import verify_password


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
