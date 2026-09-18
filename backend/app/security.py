from datetime import UTC, datetime, timedelta
from uuid import UUID

import jwt
from jwt import InvalidTokenError
from pwdlib import PasswordHash

from app.config import Settings

_password_hash = PasswordHash.recommended()
_settings = Settings()


def hash_password(password: str) -> str:
    return _password_hash.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return _password_hash.verify(password, password_hash)


def create_access_token(user_id: UUID) -> str:
    expires_at = datetime.now(UTC) + timedelta(days=_settings.access_token_days)

    return jwt.encode(
        {
            "sub": str(user_id),
            "exp": expires_at,
        },
        _settings.jwt_secret,
        algorithm=_settings.jwt_algorithm,
    )


def decode_access_token(token: str) -> UUID:
    payload = jwt.decode(
        token,
        _settings.jwt_secret,
        algorithms=[_settings.jwt_algorithm],
    )

    subject = payload.get("sub")

    if not isinstance(subject, str):
        raise InvalidTokenError("Token subject is missing.")

    try:
        return UUID(subject)
    except ValueError as error:
        raise InvalidTokenError("Token subject is invalid.") from error
