from datetime import datetime

from sqlalchemy.orm import Session

from . import models, schemas
from .auth import get_password_hash


# --- User CRUD ---
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Product CRUD ---
def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_product_by_sku(db: Session, sku: str):
    return db.query(models.Product).filter(models.Product.sku == sku).first()

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product_update: schemas.ProductCreate):
    db_product = get_product(db, product_id)
    if db_product:
        update_data = product_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_product, key, value)
        db_product.last_updated = datetime.now()
        db.commit()
        db.refresh(db_product)
    return db_product

# --- Event CRUD ---
def create_product_event(db: Session, event: schemas.EventCreate, product_id: int):
    db_product = get_product(db, product_id)
    if not db_product:
        return None # Or raise HTTPException

    db_event = models.Event(**event.model_dump(exclude={"product_id"}), product_id=product_id)
    db.add(db_event)

    # Update product's current status and last_updated
    db_product.current_status = f"{event.event_type} at {event.location}"
    db_product.last_updated = datetime.now()

    db.commit()
    db.refresh(db_event)
    db.refresh(db_product) # Refresh product to get updated status
    return db_event

def get_product_events(db: Session, product_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Event).filter(models.Event.product_id == product_id).order_by(models.Event.timestamp.desc()).offset(skip).limit(limit).all()

def get_product_with_history(db: Session, product_id: int):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product:
        events = db.query(models.Event).filter(models.Event.product_id == product_id).order_by(models.Event.timestamp.asc()).all()
        product.events = events # Attach events directly for the schema to pick up
    return product