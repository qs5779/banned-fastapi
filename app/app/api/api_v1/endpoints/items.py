from http import HTTPStatus
from typing import Any, List

from app.api import deps
from app.utils import ensure_int
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas

router = APIRouter()


@router.get("/", response_model=List[schemas.Item])
def read_items(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Retrieve items."""
    if crud.user.is_superuser(current_user):
        return crud.citem.get_multi(db, skip=skip, limit=limit)
    return crud.citem.get_multi_by_owner(
        db=db,
        owner_id=ensure_int(current_user.id, "current_user.id is None"),
        skip=skip,
        limit=limit,
    )


@router.post("/", response_model=schemas.Item)
def create_item(
    *,
    db: Session = Depends(deps.get_db),
    item_in: schemas.ItemCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Create new item."""
    cuid: int = ensure_int(current_user.id, "current_user.id is None")
    return crud.citem.create_with_owner(
        db=db,
        obj_in=item_in,
        owner_id=cuid,
    )


@router.put("/{iid}", response_model=schemas.Item)
def update_item(
    *,
    db: Session = Depends(deps.get_db),
    iid: int,
    item_in: schemas.ItemUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Update an item."""
    articulo = crud.citem.get(db=db, iid=iid)
    if not articulo:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Item not found")
    if not crud.user.is_superuser(current_user):
        if articulo.owner_id != current_user.id:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Not enough permissions",
            )
    return crud.citem.update(db=db, db_obj=articulo, obj_in=item_in)


@router.get("/{iid}", response_model=schemas.Item)
def read_item(
    *,
    db: Session = Depends(deps.get_db),
    iid: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Get item by ID."""
    articulo = crud.citem.get(db=db, iid=iid)
    if not articulo:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Item not found")
    if not crud.user.is_superuser(current_user):
        if articulo.owner_id != current_user.id:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Not enough permissions",
            )
    return articulo


@router.delete("/{iid}", response_model=schemas.Item)
def delete_item(
    *,
    db: Session = Depends(deps.get_db),
    iid: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Delete an item."""
    articulo = crud.citem.get(db=db, iid=iid)
    if not articulo:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Item not found")
    if not crud.user.is_superuser(current_user):
        if articulo.owner_id != current_user.id:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Not enough permissions",
            )
    return crud.citem.remove(db=db, iid=iid)
