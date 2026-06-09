from travel_app.database.models import (UserProfile, Category, Tour, Place,
                       Booking, Review, Gallery, RefreshToken, Favorite)
from sqladmin import ModelView


class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.id, UserProfile.full_name, UserProfile.email, UserProfile.role]


class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.id, Category.name, Category.description]


class TourAdmin(ModelView, model=Tour):
    column_list = [Tour.id, Tour.title, Tour.price, Tour.duration_days]


class PlaceAdmin(ModelView, model=Place):
    column_list = [Place.id, Place.name, Place.location, Place.coordinates]


class BookingAdmin(ModelView, model=Booking):
    column_list = [Booking.id, Booking.user_id, Booking.tour_id, Booking.status]


class ReviewAdmin(ModelView, model=Review):
    column_list = [Review.id, Review.user_id, Review.tour_id, Review.rating, Review.text]


class GalleryAdmin(ModelView, model=Gallery):
    column_list = [Gallery.id, Gallery.image_url, Gallery.place_id, Gallery.tour_id]


class RefreshTokenAdmin(ModelView, model=RefreshToken):
    column_list = [RefreshToken.id, RefreshToken.user_id, RefreshToken.created_at]


class FavoriteAdmin(ModelView, model=Favorite):
    column_list = [Favorite.id, Favorite.user_id, Favorite.tour_id]