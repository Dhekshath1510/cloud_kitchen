from sqlalchemy.orm import Session
from app.models.domain import Order, OrderItem

class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_order(self, order: Order) -> Order:
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def save_order_item(self, order_item: OrderItem) -> OrderItem:
        self.db.add(order_item)
        self.db.commit()
        self.db.refresh(order_item)
        return order_item

    def get_by_id(self, order_id: int) -> Order | None:
        return self.db.query(Order).filter(Order.order_id == order_id).first()
