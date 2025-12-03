# app/db.py

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql://postgres:1234567@localhost:5432/samsung_db"

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

class Phone(Base):
    __tablename__ = "phones"

    id = Column(Integer, primary_key=True)
    model_name = Column(String, unique=True)
    release_date = Column(String)
    display = Column(String)
    battery = Column(String)
    camera = Column(String)
    ram = Column(String)
    storage = Column(String)
    price = Column(String)

def init_db():
    Base.metadata.create_all(engine)
