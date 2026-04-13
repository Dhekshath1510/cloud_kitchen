from sqlalchemy.orm import Session
from app.models.domain import Item

class ItemRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Item]:
        return self.db.query(Item).all()

    def get_by_name(self, name: str) -> Item | None:
        return self.db.query(Item).filter(Item.item_name == name).first()
        
    def get_by_id(self, item_id: int) -> Item | None:
        return self.db.query(Item).filter(Item.item_id == item_id).first()

    def exists(self, item_id: int) -> bool:
        return self.db.query(Item).filter(Item.item_id == item_id).first() is not None

    def create(self, item: Item) -> Item:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item_id: int):
        self.db.query(Item).filter(Item.item_id == item_id).delete()
        self.db.commit()

    def save(self, item: Item) -> Item:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item
