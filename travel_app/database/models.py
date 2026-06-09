import bcrypt
from travel_app.database.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Enum, ForeignKey, DateTime, Text, Boolean, Float
from enum import Enum as PyEnum
from typing import Optional, List
from datetime import datetime


class RoleChoices(str, PyEnum):
    tourist = "tourist"
    guide = "guide"
    admin = "admin"


class BookingStatusChoices(str, PyEnum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"


class UserProfile(Base):
    __tablename__ = 'user_profiles'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    full_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    role: Mapped[RoleChoices] = mapped_column(Enum(RoleChoices), default=RoleChoices.tourist)

    reviews: Mapped[List['Review']] = relationship(back_populates='user',
                                                   cascade='all, delete-orphan')
    bookings: Mapped[List['Booking']] = relationship(back_populates='user',
                                                     cascade='all, delete-orphan')
    refresh_tokens: Mapped[List['RefreshToken']] = relationship(back_populates='user',
                                                                cascade='all, delete-orphan')
    favorites: Mapped[List['Favorite']] = relationship(back_populates='user', cascade='all, delete-orphan')

    def set_password(self, password: str):
        self.hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def __repr__(self):
        return f'{self.full_name}, {self.email}'


class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profiles.id'))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped[UserProfile] = relationship(UserProfile, back_populates='refresh_tokens')

    def __repr__(self):
        return f'RefreshToken(user_id={self.user_id})'


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    tours: Mapped[List['Tour']] = relationship(back_populates='category',
                                               cascade='all, delete-orphan')

    def __repr__(self):
        return f'{self.name}'


class Place(Base):
    __tablename__ = 'places'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    coordinates: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    tours: Mapped[List['Tour']] = relationship(back_populates='place',
                                               cascade='all, delete-orphan')
    images: Mapped[List['Gallery']] = relationship(back_populates='place',
                                                   cascade='all, delete-orphan')

    def __repr__(self):
        return f'{self.name}, {self.location}'


class Tour(Base):
    __tablename__ = 'tours'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    duration_days: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    place_id: Mapped[int] = mapped_column(ForeignKey('places.id'))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    category: Mapped[Category] = relationship(Category, back_populates='tours')
    place: Mapped[Place] = relationship(Place, back_populates='tours')
    bookings: Mapped[List['Booking']] = relationship(back_populates='tour',
                                                     cascade='all, delete-orphan')
    reviews: Mapped[List['Review']] = relationship(back_populates='tour',
                                                   cascade='all, delete-orphan')
    images: Mapped[List['Gallery']] = relationship(back_populates='tour',
                                                   cascade='all, delete-orphan')
    favorites: Mapped[List['Favorite']] = relationship(back_populates='tour', cascade='all, delete-orphan')

    def __repr__(self):
        return f'{self.title}, {self.price}'


class Booking(Base):
    __tablename__ = 'bookings'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profiles.id'))
    tour_id: Mapped[int] = mapped_column(ForeignKey('tours.id'))
    status: Mapped[BookingStatusChoices] = mapped_column(Enum(BookingStatusChoices),
                                                         default=BookingStatusChoices.pending)
    booking_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped[UserProfile] = relationship(UserProfile, back_populates='bookings')
    tour: Mapped[Tour] = relationship(Tour, back_populates='bookings')

    def __repr__(self):
        return f'Booking(user_id={self.user_id}, tour_id={self.tour_id}, status={self.status})'


class Review(Base):
    __tablename__ = 'reviews'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profiles.id'))
    tour_id: Mapped[int] = mapped_column(ForeignKey('tours.id'))
    text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    rating: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped[UserProfile] = relationship(UserProfile, back_populates='reviews')
    tour: Mapped[Tour] = relationship(Tour, back_populates='reviews')

    def __repr__(self):
        return f'Review(user_id={self.user_id}, tour_id={self.tour_id}, rating={self.rating})'


class Gallery(Base):
    __tablename__ = 'gallery'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    image_url: Mapped[str] = mapped_column(String, nullable=False)
    place_id: Mapped[Optional[int]] = mapped_column(ForeignKey('places.id'), nullable=True)
    tour_id: Mapped[Optional[int]] = mapped_column(ForeignKey('tours.id'), nullable=True)

    place: Mapped[Optional[Place]] = relationship(Place, back_populates='images')
    tour: Mapped[Optional[Tour]] = relationship(Tour, back_populates='images')

    def __repr__(self):
        return f'Gallery(place_id={self.place_id}, tour_id={self.tour_id})'


class Favorite(Base):
    __tablename__ = 'favorites'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profiles.id'))
    tour_id: Mapped[int] = mapped_column(ForeignKey('tours.id'))

    user: Mapped['UserProfile'] = relationship('UserProfile', back_populates='favorites')
    tour: Mapped['Tour'] = relationship('Tour', back_populates='favorites')

    def __repr__(self):
        return f'Favorite(user_id={self.user_id}, tour_id={self.tour_id})'