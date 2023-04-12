from typing import Any, Dict, Optional, Union

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models import User
from app.schemas import UserCreate, UserUpdate
from sqlalchemy.orm import Session


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            is_superuser=obj_in.is_superuser,
        )

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: User,
        obj_in: Union[UserUpdate, Dict[str, Any]]  # noqa
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)  # noqa
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(
        self, db: Session, email: str, password: str
    ) -> Optional[User]:  # noqa
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def disabled(self, user: User) -> bool:
        """Returns True if the user is disabled.

        :param user: user to check
        :return: True if the user is disabled
        """
        return user.disabled if user.disabled else False

    def is_superuser(self, user: User) -> bool:
        """Returns True if user is a superuser.

        :param user: user to check
        :return: True if user is a superuser
        """
        return user.is_superuser if user.is_superuser else False


user = CRUDUser(User)
