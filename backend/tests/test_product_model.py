from sqlalchemy import select

from app.models import Product, User
import pytest
from sqlalchemy.exc import IntegrityError

def test_product_can_be_persisted_for_owner(db_session):
    owner = User(
        business_name="ASI Kitchen",
        email="owner@example.com",
        password_hash="hashed-password",
    )
    product = Product(
        name="Whole milk 2L",
        owner=owner,
    )

    db_session.add(product)
    db_session.commit()

    saved_product = db_session.scalar(
        select(Product).where(Product.name == "Whole milk 2L")
    )

    assert saved_product is not None
    assert saved_product.owner_id == owner.id
    assert saved_product.owner.email == "owner@example.com"
    assert saved_product.created_at is not None
    assert saved_product.updated_at is not None


def test_product_name_must_be_unique_for_owner(db_session):
    owner = User(
        business_name="ASI Kitchen",
        email="owner@example.com",
        password_hash="hashed-password",
    )
    first_product = Product(
        name="Whole milk 2L",
        owner=owner,
    )

    db_session.add(first_product)
    db_session.commit()

    duplicate_product = Product(
        name="Whole milk 2L",
        owner=owner,
    )
    db_session.add(duplicate_product)

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()
