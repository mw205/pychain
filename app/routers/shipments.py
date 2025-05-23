from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import auth, crud, models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/events",
    tags=["events"],
    dependencies=[Depends(auth.get_current_active_user)] # All event routes require login
)

@router.post("/", response_model=schemas.Event, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(auth.require_role("distributor"))]) # Or supplier, depending on your logic
def record_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    product = crud.get_product(db, event.product_id)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with id {event.product_id} not found")

    created_event = crud.create_product_event(db=db, event=event, product_id=event.product_id)
    if not created_event:
         raise HTTPException(status_code=500, detail="Could not create event")
    return created_event

@router.get("/product/{product_id}", response_model=List[schemas.Event])
def read_product_events(product_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    events = crud.get_product_events(db, product_id=product_id, skip=skip, limit=limit)
    if not events:
        # Return empty list if no events, or 404 if product itself doesn't exist (handled in product endpoint)
        pass
    return events