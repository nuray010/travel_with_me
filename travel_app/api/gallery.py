from fastapi import APIRouter, Depends, HTTPException
from travel_app.database.models import Gallery
from travel_app.database.schema import GalleryOutSchema, GalleryInputSchema
from travel_app.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


gallery_router = APIRouter(prefix='/gallery', tags=['Gallery'])


@gallery_router.post("/", response_model=GalleryOutSchema)
async def create_gallery(gallery: GalleryInputSchema, db: Session = Depends(get_db)):
    gallery_db = Gallery(**gallery.dict())
    db.add(gallery_db)
    db.commit()
    db.refresh(gallery_db)
    return gallery_db


@gallery_router.get("/", response_model=List[GalleryOutSchema])
async def list_gallery(db: Session = Depends(get_db)):
    return db.query(Gallery).all()


@gallery_router.get('/{gallery_id}', response_model=GalleryOutSchema)
async def detail_gallery(gallery_id: int, db: Session = Depends(get_db)):
    gallery = db.query(Gallery).filter(Gallery.id == gallery_id).first()
    if not gallery:
        raise HTTPException(status_code=404, detail="мындай id сүрөт жок")
    return gallery


@gallery_router.put('/{gallery_id}', response_model=GalleryOutSchema)
async def update_gallery(gallery_id: int, gallery_data: GalleryInputSchema, db: Session = Depends(get_db)):
    gallery = db.query(Gallery).filter(Gallery.id == gallery_id).first()
    if not gallery:
        raise HTTPException(status_code=404, detail="мындай id сүрөт жок")
    for key, value in gallery_data.dict().items():
        setattr(gallery, key, value)
    db.commit()
    db.refresh(gallery)
    return gallery


@gallery_router.delete('/{gallery_id}')
async def delete_gallery(gallery_id: int, db: Session = Depends(get_db)):
    gallery = db.query(Gallery).filter(Gallery.id == gallery_id).first()
    if not gallery:
        raise HTTPException(status_code=404, detail="мындай id сүрөт жок")
    db.delete(gallery)
    db.commit()
    return {"message": "сүрөт өчүрүлдү"}