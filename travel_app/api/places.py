from fastapi import APIRouter, Depends, HTTPException
from travel_app.database.models import Place
from travel_app.database.schema import PlaceOutSchema, PlaceInputSchema
from travel_app.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


place_router = APIRouter(prefix='/places', tags=['Places'])


@place_router.post("/", response_model=PlaceOutSchema)
async def create_place(place: PlaceInputSchema, db: Session = Depends(get_db)):
    place_db = Place(**place.dict())
    db.add(place_db)
    db.commit()
    db.refresh(place_db)
    return place_db


@place_router.get("/", response_model=List[PlaceOutSchema])
async def list_places(db: Session = Depends(get_db)):
    return db.query(Place).all()


@place_router.get('/{place_id}', response_model=PlaceOutSchema)
async def detail_place(place_id: int, db: Session = Depends(get_db)):
    place = db.query(Place).filter(Place.id == place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="мындай id жер жок")
    return place


@place_router.put('/{place_id}', response_model=PlaceOutSchema)
async def update_place(place_id: int, place_data: PlaceInputSchema, db: Session = Depends(get_db)):
    place = db.query(Place).filter(Place.id == place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="мындай id жер жок")
    for key, value in place_data.dict().items():
        setattr(place, key, value)
    db.commit()
    db.refresh(place)
    return place


@place_router.delete('/{place_id}')
async def delete_place(place_id: int, db: Session = Depends(get_db)):
    place = db.query(Place).filter(Place.id == place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="мындай id жер жок")
    db.delete(place)
    db.commit()
    return {"message": "жер өчүрүлдү"}