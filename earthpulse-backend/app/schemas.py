# app/schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Forest schemas
class ForestDataBase(BaseModel):
    region: str
    forest_coverage: float
    deforestation_rate: Optional[float] = None

class ForestDataCreate(ForestDataBase):
    pass

class ForestData(ForestDataBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

# Weather schemas
class WeatherDataBase(BaseModel):
    region: str
    temperature: float
    humidity: float
    precipitation: Optional[float] = None

class WeatherDataCreate(WeatherDataBase):
    pass

class WeatherData(WeatherDataBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

# Wildfire schemas
class WildfireDataBase(BaseModel):
    region: str
    fire_risk: float
    active_fires: int
    area_affected: Optional[float] = None

class WildfireDataCreate(WildfireDataBase):
    pass

class WildfireData(WildfireDataBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True