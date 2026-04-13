from sqlalchemy.orm import Session
from app.models.domain import Discount

class DiscountRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_code(self, code: str) -> Discount | None:
        return self.db.query(Discount).filter(Discount.discount_code == code).first()

    def get_by_id(self, discount_id: int) -> Discount | None:
        return self.db.query(Discount).filter(Discount.discount_id == discount_id).first()

    def save(self, discount: Discount) -> Discount:
        self.db.add(discount)
        self.db.commit()
        self.db.refresh(discount)
        return discount
