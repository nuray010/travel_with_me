from .views import (UserProfileAdmin,GalleryAdmin,BookingAdmin,PlaceAdmin,
                    FavoriteAdmin,TourAdmin,CategoryAdmin,ReviewAdmin,RefreshTokenAdmin)
from fastapi import FastAPI
from sqladmin import Admin
from travel_app.database.db import engine

def setup_admin(travel_app: FastAPI):
    admin = Admin(travel_app, engine)
    admin.add_view(UserProfileAdmin)
    admin.add_view(CategoryAdmin)
    admin.add_view(GalleryAdmin)
    admin.add_view(ReviewAdmin)
    admin.add_view(RefreshTokenAdmin)
    admin.add_view(FavoriteAdmin)
    admin.add_view(TourAdmin)
    admin.add_view(BookingAdmin)
    admin.add_view(PlaceAdmin)


