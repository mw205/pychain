from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


# --- User Schemas ---
class UserBase(BaseModel):
    username: str
    role: str  # e.g., "supplier", "distributor", "admin"

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    disabled: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# --- Product Schemas ---
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    sku: str # Stock Keeping Unit

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    current_status: Optional[str] = "Registered"
    last_updated: datetime

    model_config = ConfigDict(from_attributes=True)

# --- Event Schemas ---



class EventTypeEnum(str, Enum):
    MANUFACTURED = "MANUFACTURED"
    PACKAGED = "PACKAGED"
    SHIPPED_FROM_SUPPLIER = "SHIPPED_FROM_SUPPLIER"
    RECEIVED_AT_WAREHOUSE = "RECEIVED_AT_WAREHOUSE"
    IN_TRANSIT_TO_DISTRIBUTOR = "IN_TRANSIT_TO_DISTRIBUTOR"
    RECEIVED_BY_DISTRIBUTOR = "RECEIVED_BY_DISTRIBUTOR"
    SHIPPED_TO_RETAILER = "SHIPPED_TO_RETAILER"
    RECEIVED_BY_RETAILER = "RECEIVED_BY_RETAILER"
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY"
    DELIVERED_TO_CUSTOMER = "DELIVERED_TO_CUSTOMER"
    INSPECTION_PASSED = "INSPECTION_PASSED"
    INSPECTION_FAILED = "INSPECTION_FAILED"
    EXCEPTION_LOGGED = "EXCEPTION_LOGGED"



class EventBase(BaseModel):
    product_id: int
    event_type: EventTypeEnum # Use the Enum here
    location: str
    notes: Optional[str] = None

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)

class ProductHistory(Product):
    events: List[Event] = []
