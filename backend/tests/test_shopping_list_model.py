from datetime import datetime, timezone

import pytest
from sqlalchemy.exc import IntegrityError
from app.models import ShoppingList, User


def test_shopping_list_is_created_active_with_share_token(
    db_session,
):
    owner = User(
        business_name="ASI Kitchen",
        email="owner@example.com",
        password_hash="hashed-password",
    )
    shopping_list = ShoppingList(owner=owner)

    db_session.add(shopping_list)
    db_session.commit()

    assert shopping_list.owner_id == owner.id
    assert shopping_list.owner.email == "owner@example.com"
    assert shopping_list.completed_at is None
    assert isinstance(shopping_list.share_token, str)
    assert len(shopping_list.share_token) >= 32
    assert shopping_list.created_at is not None


def test_owner_can_have_only_one_active_shopping_list(
    db_session,
):
    owner = User(
        business_name="ASI Kitchen",
        email="owner@example.com",
        password_hash="hashed-password",
    )
    completed_list = ShoppingList(
        owner=owner,
        completed_at=datetime.now(timezone.utc),
    )
    active_list = ShoppingList(owner=owner)

    db_session.add_all([completed_list, active_list])
    db_session.commit()

    second_active_list = ShoppingList(owner=owner)
    db_session.add(second_active_list)

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()


def test_shopping_list_share_token_is_unique(db_session):
    first_owner = User(
        business_name="ASI Kitchen",
        email="first@example.com",
        password_hash="hashed-password",
    )
    first_list = ShoppingList(
        owner=first_owner,
        share_token="shared-token",
    )

    db_session.add(first_list)
    db_session.commit()

    second_owner = User(
        business_name="Second Kitchen",
        email="second@example.com",
        password_hash="hashed-password",
    )
    second_list = ShoppingList(
        owner=second_owner,
        share_token="shared-token",
    )

    db_session.add(second_list)

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()
