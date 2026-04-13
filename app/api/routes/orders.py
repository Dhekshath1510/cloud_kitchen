from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.domain import User
from app.api.dependencies.auth import get_current_admin, get_current_customer, get_current_user
from app.services.order_service import OrderService
from app.schemas.domain import OrderRequestDto, OrderResponseDto, OrderCancelRequest, SuccessfulResponse

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("", dependencies=[Depends(get_current_user)])
def create_order(request: OrderRequestDto, db: Session = Depends(get_db)):
    service = OrderService(db)
    try:
        payment_dict = service.create_order(request)
        return payment_dict
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/cancel", response_model=SuccessfulResponse)
def cancel_order(request: OrderCancelRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = OrderService(db)
    try:
        # Validate that the token user matches the order customer name, assuming user_name represents the customer
        return service.cancel_order(request, current_user.user_name)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/admin", dependencies=[Depends(get_current_admin)])
def view_all_orders(db: Session = Depends(get_db)):
    # Using generic fetch for Admin 
    from app.models.domain import Order
    orders = db.query(Order).all()
    # Simple formatting
    return [{"order_id": o.order_id, "customer_name": o.customer_name, "total_cost": o.total_cost, "status": o.order_status} for o in orders]
