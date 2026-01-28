# app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas

# Forest CRUD operations
def get_forest_data(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ForestData).offset(skip).limit(limit).all()

def create_forest_data(db: Session, forest_data: schemas.ForestDataCreate):
    db_forest = models.ForestData(**forest_data.dict())
    db.add(db_forest)
    db.commit()
    db.refresh(db_forest)
    return db_forest

# Weather CRUD operations
def get_weather_data(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.WeatherData).offset(skip).limit(limit).all()

def create_weather_data(db: Session, weather_data: schemas.WeatherDataCreate):
    db_weather = models.WeatherData(**weather_data.dict())
    db.add(db_weather)
    db.commit()
    db.refresh(db_weather)
    return db_weather

# Wildfire CRUD operations
def get_wildfire_data(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.WildfireData).offset(skip).limit(limit).all()

def create_wildfire_data(db: Session, wildfire_data: schemas.WildfireDataCreate):
    db_wildfire = models.WildfireData(**wildfire_data.dict())
    db.add(db_wildfire)
    db.commit()
    db.refresh(db_wildfire)
    return db_wildfire