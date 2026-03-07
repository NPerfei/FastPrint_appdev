
from pydantic import BaseModel
from typing import Optional
from enum import Enum

class OrderStatus(str, Enum):
    queued = "queued"
    pending = "pending"
    cancelled = "cancelled"
    finished = "finished"

class OrderCreate(BaseModel):
    customer_name: str
    pages: int
    print_type: str

class OrderUpdateStatus(BaseModel):
    status: OrderStatus

class Order(BaseModel):
    id: int
    customer_name: str
    pages: int
    print_type: str
    cost: float
    status: OrderStatus
    created_at: str
    updated_at: str

class Pricing(BaseModel):
    id: int
    print_type: str
    price_per_page: float
    updated_at: str

class PricingUpdate(BaseModel):
    print_type: str
    price_per_page: float
