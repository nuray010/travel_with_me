from fastapi import APIRouter, Depends, HTTPException
from travel_app.database.models import Tour
from travel_app.database.schema import TourOutSchema, TourInputSchema
from travel_app.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


tour_router = APIRouter(prefix='/tours', tags=['Tours'])


@tour_router.post("/", response_model=TourOutSchema)
async def create_tour(tour: TourInputSchema, db: Session = Depends(get_db)):
    tour_db = Tour(**tour.dict())
    db.add(tour_db)
    db.commit()
    db.refresh(tour_db)
    return tour_db


@tour_router.get("/", response_model=List[TourOutSchema])
async def list_tours(db: Session = Depends(get_db)):
    return db.query(Tour).all()


@tour_router.get('/{tour_id}', response_model=TourOutSchema)
async def detail_tour(tour_id: int, db: Session = Depends(get_db)):
    tour = db.query(Tour).filter(Tour.id == tour_id).first()
    if not tour:
        raise HTTPException(status_code=404, detail="мындай id тур жок")
    return tour


@tour_router.put('/{tour_id}', response_model=TourOutSchema)
async def update_tour(tour_id: int, tour_data: TourInputSchema, db: Session = Depends(get_db)):
    tour = db.query(Tour).filter(Tour.id == tour_id).first()
    if not tour:
        raise HTTPException(status_code=404, detail="мындай id тур жок")
    for key, value in tour_data.dict().items():
        setattr(tour, key, value)
    db.commit()
    db.refresh(tour)
    return tour


@tour_router.delete('/{tour_id}')
async def delete_tour(tour_id: int, db: Session = Depends(get_db)):
    tour = db.query(Tour).filter(Tour.id == tour_id).first()
    if not tour:
        raise HTTPException(status_code=404, detail="мындай id тур жок")
    db.delete(tour)
    db.commit()
    return {"message": "тур өчүрүлдү"}