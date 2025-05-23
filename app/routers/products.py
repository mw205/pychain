from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import auth, crud, models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/products",
    tags=["products"],
    dependencies=[Depends(auth.get_current_active_user)] # All product routes require login
)

@router.post("/", response_model=schemas.Product, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(auth.require_role("supplier"))]) # Only suppliers or admins can create
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = crud.get_product_by_sku(db, sku=product.sku)
    if db_product:
        raise HTTPException(status_code=400, detail="SKU already registered")
    return crud.create_product(db=db, product=product)

@router.get("/", response_model=List[schemas.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = crud.get_products(db, skip=skip, limit=limit)
    return products

@router.get("/{product_id}", response_model=schemas.ProductHistory) # Changed to ProductHistory
def read_product_history(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product_with_history(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.put("/{product_id}", response_model=schemas.Product,
            dependencies=[Depends(auth.require_role("supplier"))]) # Only suppliers or admins can update
def update_product(product_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = crud.update_product(db, product_id=product_id, product_update=product)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product