from typing import Optional

from pydantic import BaseModel


# Shared properties
class ItemBase(BaseModel):
    """ItemBase class."""

    title: Optional[str] = None
    description: Optional[str] = None


# Properties to receive on item creation
class ItemCreate(ItemBase):
    """ItemCreate class."""

    title: str


# Properties to receive on item update
class ItemUpdate(ItemBase):
    """ItemUpdate class."""


# Properties shared by models stored in DB
class ItemInDBBase(ItemBase):
    """ItemInDBBase class."""

    id: int
    title: str
    owner_id: int

    class Config:  # noqa: WPS306
        orm_mode = True


# Properties to return to client
class Item(ItemInDBBase):  # noqa: WPS110
    """Item class."""


# Properties properties stored in DB
class ItemInDB(ItemInDBBase):
    """ItemInDB class."""
