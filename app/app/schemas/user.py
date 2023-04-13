from typing import Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    """UserBase class."""

    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    """UserCreate class."""

    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    """UserUpdate class."""

    password: Optional[str] = None


class UserInDBBase(UserBase):
    """UserInDBBase class."""

    id: Optional[int] = None

    class Config:  # noqa: WPS306
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    """User class."""


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    """UserInDB class."""

    hashed_password: str
