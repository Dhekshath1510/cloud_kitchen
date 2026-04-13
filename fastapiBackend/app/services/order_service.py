from sqlalchemy.orm import Session
from datetime import datetime

from app.repository.order_repository import OrderRepository
from app.repository.user_repository import UserRepository
from app.repository.item_repository import ItemRepository
from app.services.discount_service import DiscountService
from app.services.payment_service import PaymentService

from app.models.domain import Order, OrderItem, OrderStatus, DiscountStatus, DiscountType
from app.schemas.domain import OrderRequestDto, OrderResponseDto, OrderCancelRequest, PaymentOrderRequestDto, SuccessfulResponse

class OrderService:
    def __init__(self, db: Session):
        self.order_repo = OrderRepository(db)
        self.user_repo = UserRepository(db)
        self.item_repo = ItemRepository(db)
        self.discount_service = DiscountService(db)
        self.payment_service = PaymentService()

    def create_order(self, request_dto: OrderRequestDto) -> dict: # Returning dict to map nicely to multiple DTO aspects
        customerName = request_dto.customerName
        customer = self.user_repo.get_by_username(customerName)
        if not customer:
            raise ValueError("Invalid user!")

        order = Order(
            customer_name=customer.user_name,
            order_status=OrderStatus.PENDING,
            order_time=datetime.utcnow()
        )
        total_cost = 0.0
        
        # Save order initially to get an ID for related items
        order = self.order_repo.save_order(order)
        
        for item_info in request_dto.items:
            item = self.item_repo.get_by_name(item_info.itemName)
            if not item:
                raise ValueError(f"Item not found: {item_info.itemName}")
            if not item.is_available:
                raise ValueError(f"Item {item.item_name} is currently unavailable")

            item_total = item.price * item_info.qty
            total_cost += item_total

            order_item = OrderItem(
                order_id=order.order_id,
                item_id=item.item_id,
                quantity=item_info.qty,
                item_total_cost=item_total
            )
            self.order_repo.save_order_item(order_item)

        order.total_cost = total_cost

        if request_dto.discountCode:
            self.apply_discount(order, request_dto.discountCode)

        tax = order.total_cost * 0.05
        order.tax = tax
        self.order_repo.save_order(order)

        payment_info = self.payment_service.create_payment_order(PaymentOrderRequestDto(
            orderId=order.order_id,
            paymentMethod="CARD", # default
            amount=order.total_cost + tax
        ))
        
        # Email skipped since it requires setup 
        return {
            "orderId": order.order_id,
            "totalCost": order.total_cost + order.tax,
            "orderStatus": OrderStatus.PENDING.value,
            "tax": order.tax,
            "paymentInfo": payment_info
        }

    def cancel_order(self, cancel_request: OrderCancelRequest, requesting_customer_name: str) -> SuccessfulResponse:
        order = self.order_repo.get_by_id(cancel_request.orderId)
        if not order:
            raise ValueError(f"Order ID: {cancel_request.orderId} not found.")
        if order.customer_name != requesting_customer_name:
            raise ValueError("Invalid Customer")
            
        refund = order.total_cost - (0.1 * order.total_cost)
        order.order_status = OrderStatus.CANCELLED
        self.order_repo.save_order(order)
        
        return SuccessfulResponse(message=f"Order cancelled successfully. Your refund: Rs.{refund}")

    def apply_discount(self, order: Order, discount_code: str):
        discount = self.discount_service.get_discount(discount_code)
        
        if discount.status in [DiscountStatus.INACTIVE, DiscountStatus.EXPIRED]:
            raise ValueError("Discount currently inactive or expired.")
            
        if discount.current_usage >= discount.max_usage:
            self.discount_service.set_discount_status(discount.discount_id, DiscountStatus.EXPIRED)
            raise ValueError("Discount reached maximum use limit")
            
        if discount.min_level > order.total_cost:
            raise ValueError("Discount code cannot be applied for this order")

        if discount.discount_type == DiscountType.FLAT:
            order.total_cost = max(0, order.total_cost - discount.discount_value)
        else: # PERCENTAGE
            order.total_cost -= order.total_cost * (discount.discount_value / 100)
            
        order.discount_code = discount_code
        self.discount_service.increment_usage(discount.discount_id)
