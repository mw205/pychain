from datetime import datetime, timezone  # Import datetime and timezone

from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy import Enum as SAEnum
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base
from .schemas import EventTypeEnum


# Helper function for Python-side datetime defaults
def get_current_timezone_aware_datetime():
    return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="viewer") # e.g., supplier, distributor, admin
    disabled = Column(Boolean, default=False)

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    sku = Column(String, unique=True, index=True, nullable=False)
    current_status = Column(String, default="Registered")
    last_updated = Column(
        DateTime(timezone=True),
        default=get_current_timezone_aware_datetime,  # Changed default
        onupdate=get_current_timezone_aware_datetime # Changed onupdate
    )

    events = relationship("Event", back_populates="product", cascade="all, delete-orphan")

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    location = Column(String, nullable=False)
    event_type = Column(SAEnum(EventTypeEnum, name="event_type_enum_constraint", inherit_schema=True), nullable=False)
    notes = Column(String, nullable=True)
    timestamp = Column(
        DateTime(timezone=True),
        default=get_current_timezone_aware_datetime # Consistent datetime default
    )
    product = relationship("Product", back_populates="events")