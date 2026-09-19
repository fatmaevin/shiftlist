from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import User
from app.schemas.auth import RegisterRequest
from app.security import hash_password


class EmailAlreadyRegisteredError(Exception):
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
