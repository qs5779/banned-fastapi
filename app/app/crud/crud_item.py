from typing import List

from app.crud.base import CRUDBase
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session


class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    """CRUDItem class."""

    def create_with_owner(
        self, db: Session, *, obj_in: ItemCreate, owner_id: int,
    ) -> Item:
        """Create a new crud item.

        Args:
            db (Session): database session
            obj_in (ItemCreate): item to be created
            owner_id (int): owner id

        Returns:
            Item: Item object created
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100,
    ) -> List[Item]:
        """Get a list of crud items.

        Args:
            db (Session): database session
            owner_id (int): owner id
            skip (int, optional): number of items to skip. Defaults to 0.
            limit (int, optional): number of items to return. Defaults to 100.

        Returns:
            List[Item]: List of Item objects
        """
        return (
            db.query(self.model)
            .filter(Item.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


citem = CRUDItem(Item)
