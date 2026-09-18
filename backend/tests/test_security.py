from uuid import uuid4

import pytest
from jwt import InvalidTokenError

from app.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_password_hash_is_not_plain_text_and_verifies():
    password = "StrongPass123!"

    password_hash = hash_password(password)

    assert password_hash != password
    assert verify_password(password, password_hash) is True
    assert verify_password("WrongPass123!", password_hash) is False


def test_access_token_round_trip():
    user_id = uuid4()

    token = create_access_token(user_id)

    assert decode_access_token(token) == user_id


def test_invalid_access_token_is_rejected():
    with pytest.raises(InvalidTokenError):
        decode_access_token("not-a-valid-token")
