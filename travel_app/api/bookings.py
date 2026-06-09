from fastapi import APIRouter, Depends, HTTPException
from travel_app.database.models import Booking
from travel_app.database.schema import BookingOutSchema, BookingInputSchema
from travel_app.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


booking_router = APIRouter(prefix='/bookings', tags=['Bookings'])


@booking_router.post("/", response_model=BookingOutSchema)
async def create_booking(booking: BookingInputSchema, db: Session = Depends(get_db)):
    booking_db = Booking(**booking.dict())
    db.add(booking_db)
    db.commit()
    db.refresh(booking_db)
    return booking_db


@booking_router.get("/", response_model=List[BookingOutSchema])
async def list_bookings(db: Session = Depends(get_db)):
    return db.query(Booking).all()


@booking_router.get('/{booking_id}', response_model=BookingOutSchema)
async def detail_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="мындай id бронь жок")
    return booking


@booking_router.put('/{booking_id}', response_model=BookingOutSchema)
async def update_booking(booking_id: int, booking_data: BookingInputSchema, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="мындай id бронь жок")
    for key, value in booking_data.dict().items():
        setattr(booking, key, value)
    db.commit()
    db.refresh(booking)
    return booking


@booking_router.delete('/{booking_id}')
async def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="мындай id бронь жок")
    db.delete(booking)
    db.commit()
    return {"message": "бронь өчүрүлдү"}