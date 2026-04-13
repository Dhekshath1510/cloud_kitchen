from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.domain import User
from app.api.dependencies.auth import get_current_admin, get_current_user
from app.services.item_service import ItemService
from app.schemas.domain import ItemResponseDto, SuccessfulResponse

router = APIRouter(prefix="/menu", tags=["Menu"])

@router.get("", response_model=List[ItemResponseDto])
def get_all_items(db: Session = Depends(get_db)):
    service = ItemService(db)
    try:
        items = service.get_items()
        return [item.model_dump(by_alias=True) for item in items]
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/{name}", response_model=ItemResponseDto)
def get_item(name: str, db: Session = Depends(get_db)):
    service = ItemService(db)
    try:
        item = service.get_item(name)
        return item
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("", response_model=ItemResponseDto, dependencies=[Depends(get_current_admin)])
def add_item(item_data: dict, db: Session = Depends(get_db)):
    service = ItemService(db)
    try:
        new_item = service.add_item(item_data)
        return new_item
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{name}", response_model=SuccessfulResponse, dependencies=[Depends(get_current_admin)])
def delete_item(name: str, db: Session = Depends(get_db)):
    service = ItemService(db)
    try:
        service.delete_item(name)
        return SuccessfulResponse(message="Item deleted successfully")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put("/{name}/available", response_model=SuccessfulResponse, dependencies=[Depends(get_current_admin)])
def set_item_available(name: str, db: Session = Depends(get_db)):
    service = ItemService(db)
    try:
        service.set_to_available(name)
        return SuccessfulResponse(message="Item status updated to available")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put("/{name}/unavailable", response_model=SuccessfulResponse, dependencies=[Depends(get_current_admin)])
def set_item_unavailable(name: str, db: Session = Depends(get_db)):
    service = ItemService(db)
    try:
        service.set_to_unavailable(name)
        return SuccessfulResponse(message="Item status updated to unavailable")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
