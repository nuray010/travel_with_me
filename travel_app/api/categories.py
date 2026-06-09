from fastapi import APIRouter, Depends, HTTPException
from travel_app.database.models import Category
from travel_app.database.schema import CategoryOutSchema, CategoryInputSchema
from travel_app.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


category_router = APIRouter(prefix='/categories', tags=['Categories'])


@category_router.post("/", response_model=CategoryOutSchema)
async def create_category(category: CategoryInputSchema, db: Session = Depends(get_db)):
    category_db = Category(**category.dict())
    db.add(category_db)
    db.commit()
    db.refresh(category_db)
    return category_db


@category_router.get("/", response_model=List[CategoryOutSchema])
async def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()


@category_router.get('/{category_id}', response_model=CategoryOutSchema)
async def detail_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="мындай id категория жок")
    return category


@category_router.put('/{category_id}', response_model=CategoryOutSchema)
async def update_category(category_id: int, category_data: CategoryInputSchema, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="мындай id категория жок")
    for key, value in category_data.dict().items():
        setattr(category, key, value)
    db.commit()
    db.refresh(category)
    return category


@category_router.delete('/{category_id}')
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="мындай id категория жок")
    db.delete(category)
    db.commit()
    return {"message": "категория өчүрүлдү"}