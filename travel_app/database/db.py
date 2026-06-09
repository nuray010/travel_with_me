from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine

DB_URL = 'postgresql://postgres:admin@localhost/travel_fastapi_db'
engine = create_engine(DB_URL)

SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()