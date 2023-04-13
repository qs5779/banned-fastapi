from datetime import datetime, timedelta
from typing import Any, Optional, Union

from app.core.config import settings
from jose import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def create_access_token(
    subject: Union[str, Any],
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create a new access token."""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)


def verify_password(plain_password, hashed_password) -> bool:
    """Verify password."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    """Return the hash of the password.

    Args:
        password (_type_): password to hash

    Returns:
        str: hash of the password
    """
    return pwd_context.hash(password)
