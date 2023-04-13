from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union, cast

from app.db.database import Base
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Base class for CRUD."""

    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, iid: Any) -> Optional[ModelType]:
        """Returns query result."""
        return (
            db.query(self.model)
            .filter(self.model.id == iid)  # type: ignore [attr-defined]
            .first()
        )

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> List[ModelType]:
        """Returns query results."""
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """Create a crud item.

        Args:
            db (Session): database session
            obj_in (CreateSchemaType): item data

        Returns:
            ModelType: model item
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        """Update crud item.

        Args:
            db (Session): database session
            db_obj (ModelType): model object
            obj_in (Union[UpdateSchemaType, Dict[str, Any]]): update data

        Returns:
            ModelType: model object
        """
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data.get(field))
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, iid: int) -> ModelType:
        """Remove and return a crud item from the database.

        Args:
            db (Session): database session
            iid (int): item id

        Returns:
            ModelType: database model type
        """
        qobj = db.query(self.model).get(iid)
        db.delete(qobj)
        db.commit()
        return cast(ModelType, qobj)
