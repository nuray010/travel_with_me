from fastapi import FastAPI
import uvicorn
from travel_app.admin.setup import setup_admin
from travel_app.api import users, categories, places, tours, bookings, reviews, gallery, auth

tour_app = FastAPI(title="Tour_app")

tour_app.include_router(auth.auth_router)
tour_app.include_router(users.user_router)
tour_app.include_router(categories.category_router)
tour_app.include_router(places.place_router)
tour_app.include_router(tours.tour_router)
tour_app.include_router(bookings.booking_router)
tour_app.include_router(reviews.review_router)
tour_app.include_router(gallery.gallery_router)

setup_admin(tour_app)

if __name__ == '__main__':
    uvicorn.run(tour_app, host="127.0.0.1", port=8000)