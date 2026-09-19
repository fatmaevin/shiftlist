import pytest
from sqlalchemy.exc import IntegrityError
from app.models import (
    Product,
    ShoppingList,
    ShoppingListItem,
    User,
)


def test_catalogue_product_can_be_added_to_shopping_list(
    db_session,
):
    owner = User(
        business_name="ASI Kitchen",
        email="owner@example.com",
        password_hash="hashed-password",
    )
    product = Product(
        name="Whole milk 2L",
        owner=owner,
    )
    shopping_list = ShoppingList(owner=owner)
    item = ShoppingListItem(
        shopping_list=shopping_list,
        product=product,
        product_name=product.name,
        quantity=3,
    )

    db_session.add(item)
    db_session.commit()

    assert item.shopping_list_id == shopping_list.id
    assert item.product_id == product.id
    assert item.product_name == "Whole milk 2L"
    assert item.quantity == 3
    assert item.is_purchased is False
    assert item.shopping_list.owner_id == owner.id
    assert item.created_at is not None
    assert item.updated_at is not None


def test_shopping_list_item_quantity_must_be_positive(
    db_session,
):
    owner = User(
        business_name="ASI Kitchen",
        email="owner@example.com",
        password_hash="hashed-password",
    )
    shopping_list = ShoppingList(owner=owner)
    item = ShoppingListItem(
        shopping_list=shopping_list,
        product_name="Whole milk 2L",
        quantity=0,
    )

    db_session.add(item)

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()


def test_catalogue_product_is_unique_within_shopping_list(
    db_session,
):
    owner = User(
        business_name="ASI Kitchen",
        email="owner@example.com",
        password_hash="hashed-password",
    )
    product = Product(
        name="Whole milk 2L",
        owner=owner,
    )
    shopping_list = ShoppingList(owner=owner)
    first_item = ShoppingListItem(
        shopping_list=shopping_list,
        product=product,
        product_name=product.name,
        quantity=2,
    )

    db_session.add(first_item)
    db_session.commit()

    duplicate_item = ShoppingListItem(
        shopping_list=shopping_list,
        product=product,
        product_name=product.name,
        quantity=3,
    )
    db_session.add(duplicate_item)

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()
