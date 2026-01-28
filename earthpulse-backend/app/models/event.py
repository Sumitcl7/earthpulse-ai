# app/models/event.py
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Boolean, Text
from datetime import datetime
from app.database.connection import Base

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Event Information
    event_type = Column(String, index=True)  # wildfire, flood, deforestation, etc.
    title = Column(String, nullable=False)
    description = Column(Text)
    severity = Column(String)  # low, medium, high, critical
    
    # Location
    location_name = Column(String, index=True)
    country = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    
    # Source Information
    source_url = Column(String)
    source_type = Column(String)  # news, satellite, social_media
    published_at = Column(DateTime)
    
    # Verification Status
    is_verified = Column(Boolean, default=False)
    verification_score = Column(Float, nullable=True)  # 0.0 to 1.0
    verification_status = Column(String, default="pending")  # pending, verified, unverified, suspect
    verification_method = Column(String, nullable=True)  # satellite, manual, ai
    
    # Satellite Data
    satellite_image_url = Column(String, nullable=True)
    satellite_source = Column(String, nullable=True)  # sentinel-2, landsat, modis
    satellite_date = Column(DateTime, nullable=True)
    
    # Analysis Results
    analysis_results = Column(JSON, nullable=True)  # Store AI analysis data
    affected_area_km2 = Column(Float, nullable=True)
    confidence_score = Column(Float, nullable=True)
    
    # Raw Data
    raw_data = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SatelliteData(Base):
    __tablename__ = "satellite_data"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Location
    region_name = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    
    # Satellite Info
    satellite_source = Column(String)  # sentinel-2, landsat-8, modis
    image_id = Column(String)
    collection_date = Column(DateTime)
    
    # Analysis Type
    analysis_type = Column(String)  # ndvi, ndwi, burn_index, thermal
    
    # Results
    metrics = Column(JSON)  # Store calculated indices
    image_url = Column(String, nullable=True)
    thumbnail_url = Column(String, nullable=True)
    
    # Metadata
    cloud_coverage = Column(Float, nullable=True)
    resolution_meters = Column(Float)
    
    created_at = Column(DateTime, default=datetime.utcnow)