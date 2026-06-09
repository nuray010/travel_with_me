from fastapi import APIRouter, Depends, HTTPException
from travel_app.database.models import Favorite, Tour
from travel_app.database.schema import FavoriteOutSchema, FavoriteInputSchema
from travel_app.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


favorite_router = APIRouter(prefix='/favorites', tags=['Favorites'])


@favorite_router.post("/", response_model=FavoriteOutSchema)
async def create_favorite(favorite: FavoriteInputSchema, db: Session = Depends(get_db)):
    tour = db.query(Tour).filter(Tour.id == favorite.tour_id).first()
    if not tour:
        raise HTTPException(status_code=404, detail="мындай id  жок")
    favorite_db = Favorite(**favorite.dict())
    db.add(favorite_db)
    db.commit()
    db.refresh(favorite_db)
    return favorite_db


@favorite_router.get("/", response_model=List[FavoriteOutSchema])
async def list_favorites(db: Session = Depends(get_db)):
    return db.query(Favorite).all()


@favorite_router.get('/tour/{tour_id}', response_model=List[FavoriteOutSchema])
async def list_favorites_by_tour(tour_id: int, db: Session = Depends(get_db)):
    tour = db.query(Tour).filter(Tour.id == tour_id).first()
    if not tour:
        raise HTTPException(status_code=404, detail="мындай id тур жок")
    return db.query(Favorite).filter(Favorite.tour_id == tour_id).all()


@favorite_router.get('/{favorite_id}', response_model=FavoriteOutSchema)
async def detail_favorite(favorite_id: int, db: Session = Depends(get_db)):
    favorite = db.query(Favorite).filter(Favorite.id == favorite_id).first()
    if not favorite:
        raise HTTPException(status_code=404, detail="мындай id favorite жок")
    return favorite


@favorite_router.delete('/{favorite_id}')
async def delete_favorite(favorite_id: int, db: Session = Depends(get_db)):
    favorite = db.query(Favorite).filter(Favorite.id == favorite_id).first()
    if not favorite:
        raise HTTPException(status_code=404, detail="мындай id favorite жок")
    db.delete(favorite)
    db.commit()
    return {"message": " favorite өчүрүлдү"}