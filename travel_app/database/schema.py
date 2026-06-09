from pydantic import BaseModel, EmailStr
from typing import Optional
from .models import RoleChoices, BookingStatusChoices
from datetime import datetime


class UserProfileOutSchema(BaseModel):
    id: int
    full_name: Optional[str]
    email: EmailStr
    is_active: bool
    is_superuser: bool
    role: RoleChoices

    class Config:
        from_attributes = True


class UserProfileInputSchema(BaseModel):
    full_name: Optional[str]
    email: EmailStr
    hashed_password: str
    role: Optional[RoleChoices] = RoleChoices.tourist


class UserLoginSchema(BaseModel):
    email: EmailStr
    hashed_password: str


class RefreshTokenOutSchema(BaseModel):
    id: int
    token: str
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class CategoryOutSchema(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        from_attributes = True


class CategoryInputSchema(BaseModel):
    name: str
    description: Optional[str]


class PlaceOutSchema(BaseModel):
    id: int
    name: str
    description: Optional[str]
    location: Optional[str]
    coordinates: Optional[str]

    class Config:
        from_attributes = True


class PlaceInputSchema(BaseModel):
    name: str
    description: Optional[str]
    location: Optional[str]
    coordinates: Optional[str]


class TourOutSchema(BaseModel):
    id: int
    title: str
    description: Optional[str]
    price: float
    duration_days: Optional[int]
    category_id: int
    place_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class TourInputSchema(BaseModel):
    title: str
    description: Optional[str]
    price: float
    duration_days: Optional[int]
    category_id: int
    place_id: int


class BookingOutSchema(BaseModel):
    id: int
    user_id: int
    tour_id: int
    status: BookingStatusChoices
    booking_date: datetime

    class Config:
        from_attributes = True


class BookingInputSchema(BaseModel):
    user_id: int
    tour_id: int
    status: Optional[BookingStatusChoices] = BookingStatusChoices.pending


class ReviewOutSchema(BaseModel):
    id: int
    user_id: int
    tour_id: int
    text: Optional[str]
    rating: int
    created_at: datetime

    class Config:
        from_attributes = True


class ReviewInputSchema(BaseModel):
    user_id: int
    tour_id: int
    text: Optional[str]
    rating: int


class GalleryOutSchema(BaseModel):
    id: int
    image_url: str
    place_id: Optional[int]
    tour_id: Optional[int]

    class Config:
        from_attributes = True


class GalleryInputSchema(BaseModel):
    image_url: str
    place_id: Optional[int]
    tour_id: Optional[int]


class FavoriteInputSchema(BaseModel):
    user_id: int
    tour_id: int


class FavoriteOutSchema(BaseModel):
    id: int
    user_id: int
    tour_id: int

    class Config:
        from_attributes = True