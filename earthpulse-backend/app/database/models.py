from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from datetime import datetime
from .connection import Base

class ForestAnalysis(Base):
    __tablename__ = "forest_analysis"
    
    id = Column(Integer, primary_key=True, index=True)
    region = Column(String, index=True)
    analysis_type = Column(String)
    data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
class WeatherData(Base):
    __tablename__ = "weather_data"
    
    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, index=True)
    temperature = Column(Float)
    humidity = Column(Float)
    data = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)

class WildfireAlert(Base):
    __tablename__ = "wildfire_alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, index=True)
    severity = Column(String)
    data = Column(JSON)
    detected_at = Column(DateTime, default=datetime.utcnow)