from http import HTTPStatus
from typing import Generator

from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import crud, models, schemas

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="{0}/login/access-token".format(settings.API_V1_STR),
)


def get_db() -> Generator:  # type: ignore [type-arg]
    """Returns the database object."""
    try:  # noqa: WPS501
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(reusable_oauth2),
) -> models.User:
    """Returns the current user."""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[security.ALGORITHM],
        )
        token_data = schemas.TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = crud.user.get(db, iid=token_data.sub)
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return user


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    """Returns the current user if user is enabled/active."""
    if crud.user.disabled(current_user):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    """Returns the current user if is a superuser."""
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="The user doesn't have enough privileges",
        )
    return current_user
