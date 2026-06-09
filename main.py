from fastapi import FastAPI
import uvicorn
from travel_app.admin.setup import setup_admin
from travel_app.api import users, categories, places, tours, bookings, reviews, gallery, auth

travel_app = FastAPI(title="Tour_app")

travel_app.include_router(auth.auth_router)
travel_app.include_router(users.user_router)
travel_app.include_router(categories.category_router)
travel_app.include_router(places.place_router)
travel_app.include_router(tours.tour_router)
travel_app.include_router(bookings.booking_router)
travel_app.include_router(reviews.review_router)
travel_app.include_router(gallery.gallery_router)

setup_admin(travel_app)

if __name__ == '__main__':
    uvicorn.run(travel_app, host="127.0.0.1", port=8000)