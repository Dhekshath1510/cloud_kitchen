from sqlalchemy.orm import Session
from app.repository.item_repository import ItemRepository
from app.models.domain import Item
from app.schemas.domain import ItemResponseDto

class ItemService:
    def __init__(self, db: Session):
        self.repo = ItemRepository(db)

    def get_items(self) -> list[ItemResponseDto]:
        items = self.repo.get_all()
        if not items:
            raise ValueError("No items found in menu")
        
        return [ItemResponseDto.model_validate(item) for item in items]

    def get_item(self, name: str) -> Item:
        item = self.repo.get_by_name(name)
        if not item:
            raise ValueError(f"Item {name} not found")
        return item

    def add_item(self, item_data: dict) -> Item:
        if "item_id" in item_data and self.repo.exists(item_data["item_id"]):
            raise ValueError(f"Item {item_data['item_name']} already exists")
        
        new_item = Item(**item_data)
        return self.repo.create(new_item)

    def delete_item(self, name: str):
        item = self.repo.get_by_name(name)
        if not item:
            raise ValueError("Item not found")
        self.repo.delete(item.item_id)

    def set_to_available(self, item_name: str):
        item = self.repo.get_by_name(item_name)
        if not item:
            raise ValueError("Item not found")
        item.is_available = True
        self.repo.save(item)

    def set_to_unavailable(self, item_name: str):
        item = self.repo.get_by_name(item_name)
        if not item:
            raise ValueError("Item not found")
        item.is_available = False
        self.repo.save(item)
