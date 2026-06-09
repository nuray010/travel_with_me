from fastapi import APIRouter, Depends, HTTPException
from travel_app.database.models import UserProfile
from travel_app.database.schema import UserProfileOutSchema, UserProfileInputSchema
from travel_app.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


user_router = APIRouter(prefix='/users', tags=['Users'])


@user_router.post("/", response_model=UserProfileOutSchema)
async def create_user(user: UserProfileInputSchema, db: Session = Depends(get_db)):
    user_data = user.dict()
    password = user_data.pop("password")
    user_db = UserProfile(**user_data)
    user_db.set_password(password)
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db


@user_router.get("/", response_model=List[UserProfileOutSchema])
async def list_users(db: Session = Depends(get_db)):
    return db.query(UserProfile).all()


@user_router.get('/{user_id}', response_model=UserProfileOutSchema)
async def detail_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="мындай id колдонуучу жок")
    return user


@user_router.put('/{user_id}', response_model=UserProfileOutSchema)
async def update_user(user_id: int, user_data: UserProfileInputSchema, db: Session = Depends(get_db)):
    user = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="мындай id колдонуучу жок")
    data = user_data.dict()
    password = data.pop("password")
    for key, value in data.items():
        setattr(user, key, value)
    user.set_password(password)
    db.commit()
    db.refresh(user)
    return user


@user_router.delete('/{user_id}')
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="мындай id колдонуучу жок")
    db.delete(user)
    db.commit()
    return {"message": "колдонуучу өчүрүлдү"}