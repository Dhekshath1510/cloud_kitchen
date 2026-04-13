import enum
from sqlalchemy import Column, String, Integer, BigInteger, Float, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
import datetime

from app.db.base import Base

class Role(str, enum.Enum):
    ROLE_USER = "ROLE_USER"
    ROLE_ADMIN = "ROLE_ADMIN"

class ItemCategory(str, enum.Enum):
    STARTER = "STARTER"
    MAIN_COURSE = "MAIN_COURSE"
    DESSERT = "DESSERT"
    BEVERAGE = "BEVERAGE"
    SNACKS = "SNACKS"
    SALAD = "SALAD"
    SOUP = "SOUP"
    ADD_ON = "ADD_ON"
    PIZZA = "PIZZA"
    BURGER = "BURGER"
    SANDWICH = "SANDWICH"
    PASTA = "PASTA"

class OrderStatus(str, enum.Enum):
    PENDING = "PENDING"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    CONFIRMED = "CONFIRMED"
    PROCESSING = "PROCESSING"
    DELIVERED = "DELIVERED"
    SHIPPED = "SHIPPED"

class PaymentStatus(str, enum.Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"

class PaymentMethod(str, enum.Enum):
    UPI = "UPI"
    CARD = "CARD"
    NET_BANKING = "NET_BANKING"
    WALLET = "WALLET"

class DiscountType(str, enum.Enum):
    FLAT = "FLAT"
    PERCENTAGE = "PERCENTAGE"

class DiscountStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    EXPIRED = "EXPIRED"

class User(Base):
    __tablename__ = "users"
    
    user_id = Column("user_id", String, primary_key=True)
    user_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(Role), nullable=False)

class Item(Base):
    __tablename__ = "items"
    
    item_id = Column(BigInteger, primary_key=True, autoincrement=True)
    item_name = Column(String, nullable=False)
    description = Column(String)
    image_url = Column(String)
    price = Column(Float, nullable=False)
    is_available = Column(Boolean, default=True)
    is_veg = Column(Boolean, default=True)
    category = Column(Enum(ItemCategory))

class Order(Base):
    __tablename__ = "orders"
    
    order_id = Column(BigInteger, primary_key=True, autoincrement=True)
    customer_name = Column(String)
    order_time = Column(DateTime, default=datetime.datetime.utcnow)
    tax = Column(Float, default=0.0)
    total_cost = Column(Float, nullable=False)
    discount_code = Column(String)
    order_status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    order_id = Column(BigInteger, ForeignKey("orders.order_id"))
    item_id = Column(BigInteger, ForeignKey("items.item_id"))
    quantity = Column(Integer, nullable=False)
    item_total_cost = Column(Float, nullable=False)
    
    order = relationship("Order", back_populates="order_items")
    item = relationship("Item")

class Payment(Base):
    __tablename__ = "payments"
    
    payment_id = Column(String, primary_key=True)
    order_id = Column(BigInteger, nullable=False)
    user_id = Column(String, nullable=False)
    gateway_reference_id = Column(String)
    amount = Column(Float, nullable=False)
    payment_status = Column(Enum(PaymentStatus), nullable=False)
    payment_method = Column(Enum(PaymentMethod))
    payment_time = Column(DateTime)

class Discount(Base):
    __tablename__ = "discounts"
    
    discount_id = Column(BigInteger, primary_key=True, autoincrement=True)
    discount_code = Column(String, unique=True, nullable=False)
    discount_type = Column(Enum(DiscountType), nullable=False)
    discount_value = Column(Float, nullable=False)
    min_level = Column(Float, default=0.0)
    status = Column(Enum(DiscountStatus), default=DiscountStatus.ACTIVE)
    issued_at = Column(DateTime)
    max_usage = Column(Integer, default=1)
    current_usage = Column(Integer, default=0)

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    
    id = Column(String, primary_key=True)
    user_email = Column(String, nullable=False)
    refresh_token = Column(String, nullable=False)
    expires_in = Column(DateTime, nullable=False)
