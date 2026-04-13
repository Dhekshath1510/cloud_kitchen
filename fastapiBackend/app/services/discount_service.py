from sqlalchemy.orm import Session
from app.repository.discount_repository import DiscountRepository
from app.models.domain import Discount, DiscountStatus

class DiscountService:
    def __init__(self, db: Session):
        self.repo = DiscountRepository(db)

    def get_discount(self, code: str) -> Discount:
        discount = self.repo.get_by_code(code)
        if not discount:
            raise ValueError(f"Discount {code} not found")
        return discount

    def set_discount_status(self, discount_id: int, status: DiscountStatus):
        discount = self.repo.get_by_id(discount_id)
        if not discount:
            raise ValueError("Discount not found")
        discount.status = status
        self.repo.save(discount)

    def increment_usage(self, discount_id: int):
        discount = self.repo.get_by_id(discount_id)
        if not discount:
            raise ValueError("Discount not found")
        discount.current_usage += 1
        self.repo.save(discount)
