from fastapi import APIRouter, HTTPException, Depends
from travel_app.database.db import SessionLocal
from travel_app.database.models import UserProfile, RefreshToken
from travel_app.database.schema import UserProfileInputSchema, UserLoginSchema
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from config import (SECRET_KEY, ALGORITHM,
                    ACCESS_TOKEN_LIFETIME,
                    REFRESH_TOKEN_LIFETIME)
from datetime import timedelta, datetime
from jose import jwt
from typing import Optional


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")

auth_router = APIRouter(prefix='/auth', tags=['Auth'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_password_hash(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:

        return False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expires = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_LIFETIME))
    to_encode.update({"exp": expires})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict):
    return create_access_token(data, expires_delta=timedelta(days=REFRESH_TOKEN_LIFETIME))


@auth_router.post('/register/', response_model=dict)
async def register(user: UserProfileInputSchema, db: Session = Depends(get_db)):
    email_db = db.query(UserProfile).filter(UserProfile.email == user.email).first()
    if email_db:
        raise HTTPException(detail='Мындай email бар экен', status_code=400)
    hash_password = get_password_hash(user.hashed_password)

    user_data = UserProfile(
        full_name=user.full_name,
        email=user.email,
        hashed_password=hash_password,
        role=user.role
    )
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return {'message': 'Сиз регистрация болдунуз'}


@auth_router.post('/login/', response_model=dict)
async def login(user: UserLoginSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.email == user.email).first()

    if not user_db or not verify_password(user.hashed_password, user_db.hashed_password):
        raise HTTPException(detail='Сиз жазган маалымат туура эмес', status_code=401)

    access_token = create_access_token({'sub': user_db.email})
    refresh_token = create_refresh_token({'sub': user_db.email})

    token_db = RefreshToken(user_id=user_db.id, token=refresh_token)
    db.add(token_db)
    db.commit()

    return {'access_token': access_token, 'refresh_token': refresh_token, 'token_type': 'Bearer'}


@auth_router.post('/logout')
async def logout(refresh_token: str, db: Session = Depends(get_db)):
    stored_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()

    if not stored_token:
        raise HTTPException(status_code=401, detail="Маалымыт туура эмес")

    db.delete(stored_token)
    db.commit()

    return {"message": "Сиз чыктыңыз"}


@auth_router.post('/refresh')
async def refresh(refresh_token: str, db: Session = Depends(get_db)):
    stored_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
    if not stored_token:
        raise HTTPException(status_code=401, detail="Маалымат ката")

    user_db = db.query(UserProfile).filter(UserProfile.id == stored_token.user_id).first()
    if not user_db:
        raise HTTPException(status_code=401, detail="Колдонуучу табылган жок")

    access_token = create_access_token({'sub': user_db.email})
    return {'access_token': access_token, 'token_type': 'Bearer'}