from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    """Token class."""

    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    """TokenPayload class."""

    sub: Optional[int] = None
