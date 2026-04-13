from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from app.models.domain import Role, ItemCategory, OrderStatus, PaymentStatus, PaymentMethod, DiscountType, DiscountStatus

# Auth & User DTOs
class UserLoginDto(BaseModel):
    userName: str
    password: str
    role: Role

class NewUserDto(UserLoginDto):
    emailId: EmailStr

class AuthResponse(BaseModel):
    accessToken: str
    refreshToken: str
    role: Role
    
class RefreshTokenRequestDto(BaseModel):
    refreshToken: str

# Item DTOs
class ItemInfoDto(BaseModel):
    itemName: str
    qty: int

class ItemResponseDto(BaseModel):
    item_id: int = Field(alias="itemId")
    item_name: str = Field(alias="itemName")
    description: Optional[str] = None
    image_url: Optional[str] = Field(alias="imageUrl")
    price: float
    is_available: bool = Field(alias="isAvailable")
    is_veg: bool = Field(alias="isVeg")
    category: Optional[ItemCategory] = None

    class Config:
        from_attributes = True
        populate_by_name = True
        allow_population_by_field_name = True

# Order DTOs
class OrderRequestDto(BaseModel):
    customerName: str
    items: List[ItemInfoDto]
    discountCode: Optional[str] = None

class OrderResponseDto(BaseModel):
    orderId: int = Field(alias="order_id")
    customerName: str = Field(alias="customer_name")
    orderTime: datetime = Field(alias="order_time")
    tax: float
    totalCost: float = Field(alias="total_cost")
    discountCode: Optional[str] = Field(None, alias="discount_code")
    orderStatus: OrderStatus = Field(alias="order_status")

    class Config:
        from_attributes = True
        populate_by_name = True

class OrderCancelRequest(BaseModel):
    orderId: int

# Payment DTOs
class PaymentOrderRequestDto(BaseModel):
    orderId: int
    paymentMethod: PaymentMethod
    amount: float

class PaymentVerificationRequestDto(BaseModel):
    paymentId: str
    orderId: int
    gatewayReferenceId: str
    status: PaymentStatus

# Discount DTOs
class DiscountInfoDto(BaseModel):
    discountCode: str
    discountType: DiscountType
    discountValue: float
    minLevel: float

# Generic Responses
class SuccessfulResponse(BaseModel):
    message: str
    
class ExceptionResponse(BaseModel):
    error: str
    details: Optional[str] = None
