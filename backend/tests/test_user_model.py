import pytest
from sqlalchemy.exc import IntegrityError

from sqlalchemy import select

from app.models.user import User


def test_user_can_be_persisted(db_session):
    user = User(
        business_name="ASI Kitchen",
        email="owner@example.com",
        password_hash="hashed-value",
    )

    db_session.add(user)
    db_session.commit()

    saved_user = db_session.scalar(
        select(User).where(User.email == "owner@example.com")
    )

    assert saved_user is not None
    assert saved_user.business_name == "ASI Kitchen"


def test_user_email_is_unique(db_session):
    db_session.add_all(
        [
            User(
                business_name="First Business",
                email="same@example.com",
                password_hash="hash-one",
            ),
            User(
                business_name="Second Business",
                email="same@example.com",
                password_hash="hash-two",
            ),
        ]
    )

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()
