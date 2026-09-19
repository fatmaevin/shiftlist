from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies.auth import get_current_user

from app.database import get_db
from app.models import User
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from app.security import create_access_token
from app.services.auth import (
    EmailAlreadyRegisteredError,
    InvalidCredentialsError,
    authenticate_user,
    register_user,
)

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_manager(
    registration: RegisterRequest,
    session: Annotated[Session, Depends(get_db)],
) -> User:
    try:
        return register_user(session, registration)
    except EmailAlreadyRegisteredError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        ) from error


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login_manager(
    credentials: LoginRequest,
    session: Annotated[Session, Depends(get_db)],
) -> TokenResponse:
    try:
        user = authenticate_user(session, credentials)
    except InvalidCredentialsError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        ) from error

    return TokenResponse(
        access_token=create_access_token(user.id),
    )


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_authenticated_manager(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    return current_user
