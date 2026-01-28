# app/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .database import Base

class ForestData(Base):
    __tablename__ = "forest_data"

    id = Column(Integer, primary_key=True, index=True)
    region = Column(String, index=True)
    forest_coverage = Column(Float)
    deforestation_rate = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, index=True)
    region = Column(String, index=True)
    temperature = Column(Float)
    humidity = Column(Float)
    precipitation = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

class WildfireData(Base):
    __tablename__ = "wildfire_data"

    id = Column(Integer, primary_key=True, index=True)
    region = Column(String, index=True)
    fire_risk = Column(Float)
    active_fires = Column(Integer)
    area_affected = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)