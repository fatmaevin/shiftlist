from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import User
from app.schemas.auth import LoginRequest, RegisterRequest
from app.security import hash_password, verify_password

class EmailAlreadyRegisteredError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


def register_user(
    session: Session,
    registration: RegisterRequest,
) -> User:
    existing_user = session.scalar(
        select(User).where(User.email == str(registration.email))
    )

    if existing_user is not None:
        raise EmailAlreadyRegisteredError

    user = User(
        business_name=registration.business_name,
        email=str(registration.email),
        password_hash=hash_password(registration.password),
    )

    session.add(user)

    try:
        session.commit()
    except IntegrityError as error:
        session.rollback()
        raise EmailAlreadyRegisteredError from error

    session.refresh(user)

    return user


def authenticate_user(
    session: Session,
    credentials: LoginRequest,
) -> User:
    user = session.scalar(select(User).where(User.email == str(credentials.email)))

    if user is None or not verify_password(
        credentials.password,
        user.password_hash,
    ):
        raise InvalidCredentialsError

    return user
