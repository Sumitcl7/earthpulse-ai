# app/main.py
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import logging
from datetime import datetime

from app.database.connection import get_db, init_db, Base, engine
from app.models.event import Event, SatelliteData
from app.services.earth_engine import earth_engine_service
from app.services.news_scraper import news_scraper_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="EarthPulse AI API",
    description="Environmental monitoring with satellite data and AI",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    try:
        init_db()
        logger.info("✅ Database initialized successfully")
    except Exception as e:
        logger.error(f"❌ Database initialization error: {e}")

@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "message": "Welcome to EarthPulse AI API",
        "status": "online",
        "docs": "/docs",
        "features": [
            "Satellite data analysis (Google Earth Engine)",
            "Environmental news scraping",
            "Event verification",
            "Real-time monitoring"
        ]
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "earth_engine": earth_engine_service.initialized,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/api/events/create")
def create_event(
    event_type: str,
    title: str,
    description: str,
    severity: str,
    location_name: str,
    latitude: float,
    longitude: float,
    country: str = None,
    source_url: str = None,
    source_type: str = "manual",
    db: Session = Depends(get_db)
):
    """
    Manually create an event for testing
    """
    event = Event(
        event_type=event_type,
        title=title,
        description=description,
        severity=severity,
        location_name=location_name,
        country=country,
        latitude=latitude,
        longitude=longitude,
        source_url=source_url,
        source_type=source_type,
        published_at=datetime.utcnow(),
        verification_status='pending',
        is_verified=False
    )
    
    db.add(event)
    db.commit()
    db.refresh(event)
    
    return {
        "message": "Event created successfully",
        "event_id": event.id,
        "event": {
            "id": event.id,
            "event_type": event.event_type,
            "title": event.title,
            "location": location_name
        }
    }

# ==================== SATELLITE ENDPOINTS ====================

@app.get("/api/satellite/ndvi")
def get_ndvi_analysis(
    latitude: float = Query(..., description="Latitude"),
    longitude: float = Query(..., description="Longitude"),
    radius_km: float = Query(10, description="Analysis radius in kilometers"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    Get vegetation health analysis using NDVI
    """
    result = earth_engine_service.get_ndvi(
        latitude, longitude, start_date, end_date, radius_km
    )
    
    # Save to database
    if "error" not in result:
        satellite_data = SatelliteData(
            region_name=f"lat{latitude}_lon{longitude}",
            latitude=latitude,
            longitude=longitude,
            satellite_source="sentinel-2",
            collection_date=datetime.utcnow(),
            analysis_type="ndvi",
            metrics=result,
            resolution_meters=10
        )
        db.add(satellite_data)
        db.commit()
    
    return result

@app.get("/api/satellite/wildfire")
def detect_wildfire(
    latitude: float = Query(..., description="Latitude"),
    longitude: float = Query(..., description="Longitude"),
    radius_km: float = Query(50, description="Detection radius in kilometers"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    Detect wildfires using thermal satellite data
    """
    result = earth_engine_service.detect_wildfires(
        latitude, longitude, start_date, end_date, radius_km
    )
    
    # Save to database
    if "error" not in result and result.get("fire_detected"):
        satellite_data = SatelliteData(
            region_name=f"lat{latitude}_lon{longitude}",
            latitude=latitude,
            longitude=longitude,
            satellite_source="modis",
            collection_date=datetime.utcnow(),
            analysis_type="wildfire_detection",
            metrics=result,
            resolution_meters=1000
        )
        db.add(satellite_data)
        db.commit()
    
    return result

@app.get("/api/satellite/water")
def detect_water_changes(
    latitude: float = Query(..., description="Latitude"),
    longitude: float = Query(..., description="Longitude"),
    radius_km: float = Query(20, description="Analysis radius in kilometers"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    Detect flood or drought using water index analysis
    """
    result = earth_engine_service.detect_water_changes(
        latitude, longitude, start_date, end_date, radius_km
    )
    
    # Save to database
    if "error" not in result:
        satellite_data = SatelliteData(
            region_name=f"lat{latitude}_lon{longitude}",
            latitude=latitude,
            longitude=longitude,
            satellite_source="sentinel-2",
            collection_date=datetime.utcnow(),
            analysis_type="water_detection",
            metrics=result,
            resolution_meters=10
        )
        db.add(satellite_data)
        db.commit()
    
    return result

# ==================== NEWS SCRAPING ENDPOINTS ====================

@app.post("/api/news/scrape")
async def scrape_environmental_news(
    background_tasks: BackgroundTasks,
    query: str = Query("wildfire OR flood OR deforestation", description="Search query"),
    max_results: int = Query(20, description="Maximum number of articles"),
    db: Session = Depends(get_db)
):
    """
    Scrape environmental news and save to database
    """
    def scrape_and_save():
        articles = news_scraper_service.scrape_google_news(query, max_results)
        
        saved_count = 0
        for article in articles:
            try:
                # Get primary location
                locations = article.get('locations', [])
                if not locations:
                    continue
                
                primary_location = locations[0]
                
                # Create event
                event = Event(
                    event_type=article['event_type'],
                    title=article['title'],
                    description=article['description'],
                    severity=article['severity'],
                    location_name=primary_location['name'],
                    latitude=primary_location['latitude'],
                    longitude=primary_location['longitude'],
                    source_url=article['url'],
                    source_type='news',
                    published_at=article['published_at'],
                    verification_status='pending',
                    raw_data=article
                )
                
                db.add(event)
                db.commit()
                saved_count += 1
                
            except Exception as e:
                logger.error(f"Error saving article: {e}")
                continue
        
        logger.info(f"Saved {saved_count} events to database")
    
    background_tasks.add_task(scrape_and_save)
    
    return {
        "message": "News scraping started",
        "status": "processing",
        "query": query
    }

# ==================== EVENT ENDPOINTS ====================

@app.get("/api/events")
def get_events(
    skip: int = Query(0, description="Skip records"),
    limit: int = Query(100, description="Limit records"),
    event_type: Optional[str] = Query(None, description="Filter by event type"),
    severity: Optional[str] = Query(None, description="Filter by severity"),
    verified_only: bool = Query(False, description="Show only verified events"),
    db: Session = Depends(get_db)
):
    """
    Get list of environmental events
    """
    query = db.query(Event)
    
    if event_type:
        query = query.filter(Event.event_type == event_type)
    
    if severity:
        query = query.filter(Event.severity == severity)
    
    if verified_only:
        query = query.filter(Event.is_verified == True)
    
    query = query.order_by(Event.created_at.desc())
    events = query.offset(skip).limit(limit).all()
    
    return [
        {
            "id": event.id,
            "event_type": event.event_type,
            "title": event.title,
            "description": event.description[:200],
            "severity": event.severity,
            "location": {
                "name": event.location_name,
                "latitude": event.latitude,
                "longitude": event.longitude
            },
            "source_url": event.source_url,
            "published_at": event.published_at.isoformat() if event.published_at else None,
            "is_verified": event.is_verified,
            "verification_status": event.verification_status,
            "created_at": event.created_at.isoformat()
        }
        for event in events
    ]

@app.get("/api/events/{event_id}")
def get_event_detail(event_id: int, db: Session = Depends(get_db)):
    """
    Get detailed information about a specific event
    """
    event = db.query(Event).filter(Event.id == event_id).first()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    return {
        "id": event.id,
        "event_type": event.event_type,
        "title": event.title,
        "description": event.description,
        "severity": event.severity,
        "location": {
            "name": event.location_name,
            "country": event.country,
            "latitude": event.latitude,
            "longitude": event.longitude
        },
        "source_url": event.source_url,
        "source_type": event.source_type,
        "published_at": event.published_at.isoformat() if event.published_at else None,
        "is_verified": event.is_verified,
        "verification_status": event.verification_status,
        "verification_score": event.verification_score,
        "satellite_image_url": event.satellite_image_url,
        "analysis_results": event.analysis_results,
        "raw_data": event.raw_data,
        "created_at": event.created_at.isoformat(),
        "updated_at": event.updated_at.isoformat()
    }

@app.post("/api/events/{event_id}/verify")
async def verify_event_with_satellite(
    event_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Verify an event using satellite data
    """
    event = db.query(Event).filter(Event.id == event_id).first()
    
    if not event:
        raise HTTPException(
            status_code=404,
            detail=f"Event with ID {event_id} not found"
        )
    
    def verify():
        try:
            logger.info(f"🔍 Starting verification for event {event_id}: {event.title}")
            
            result = None
            verified = False
            score = 0.5
            
            # Perform satellite analysis based on event type
            if event.event_type == 'wildfire':
                logger.info(f"🔥 Checking for wildfire at ({event.latitude}, {event.longitude})")
                result = earth_engine_service.detect_wildfires(
                    event.latitude, event.longitude, radius_km=50
                )
                if "error" in result:
                    logger.error(f"Error in fire detection: {result['error']}")
                    verified = False
                    score = 0.0
                else:
                    verified = result.get('fire_detected', False)
                    score = 0.9 if verified else 0.2
                    logger.info(f"Fire detection result: {verified} (score: {score})")
                
            elif event.event_type == 'flood':
                logger.info(f"💧 Checking for flood at ({event.latitude}, {event.longitude})")
                result = earth_engine_service.detect_water_changes(
                    event.latitude, event.longitude, radius_km=20
                )
                if "error" in result:
                    logger.error(f"Error in water detection: {result['error']}")
                    verified = False
                    score = 0.0
                else:
                    verified = result.get('water_present', False)
                    score = 0.8 if verified else 0.3
                    logger.info(f"Water detection result: {verified} (score: {score})")
                
            elif event.event_type == 'deforestation':
                logger.info(f"🌳 Checking for deforestation at ({event.latitude}, {event.longitude})")
                result = earth_engine_service.get_ndvi(
                    event.latitude, event.longitude, radius_km=10
                )
                if "error" in result:
                    logger.error(f"Error in NDVI calculation: {result['error']}")
                    verified = False
                    score = 0.0
                else:
                    ndvi = result.get('ndvi_mean', 1.0)
                    if ndvi is not None:
                        verified = ndvi < 0.3  # Low NDVI indicates deforestation
                        score = 0.85 if verified else 0.25
                        logger.info(f"NDVI: {ndvi}, Deforestation detected: {verified} (score: {score})")
                    else:
                        verified = False
                        score = 0.0
                        logger.warning(f"No NDVI data available")
                
            elif event.event_type == 'drought':
                logger.info(f"☀️ Checking for drought at ({event.latitude}, {event.longitude})")
                result = earth_engine_service.detect_water_changes(
                    event.latitude, event.longitude, radius_km=20
                )
                if "error" in result:
                    logger.error(f"Error in water detection: {result['error']}")
                    verified = False
                    score = 0.0
                else:
                    ndwi = result.get('ndwi_mean', 0.5)
                    if ndwi is not None:
                        verified = ndwi < 0.0  # Low NDWI indicates drought
                        score = 0.8 if verified else 0.3
                        logger.info(f"NDWI: {ndwi}, Drought detected: {verified} (score: {score})")
                    else:
                        verified = False
                        score = 0.0
                        logger.warning(f"No NDWI data available")
            else:
                result = {"message": f"Event type '{event.event_type}' not supported for automatic verification"}
                verified = False
                score = 0.5
                logger.warning(f"Unsupported event type: {event.event_type}")
            
            # Update event in database
            event.is_verified = verified
            event.verification_score = score
            event.verification_status = 'verified' if verified else 'unverified'
            event.verification_method = 'satellite'
            event.analysis_results = result
            event.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(event)
            
            logger.info(f"✅ Event {event_id} verification complete: {verified} (score: {score})")
            
        except Exception as e:
            logger.error(f"❌ Error verifying event {event_id}: {e}")
            import traceback
            logger.error(traceback.format_exc())
            db.rollback()
    
    background_tasks.add_task(verify)
    
    return {
        "message": "Verification started",
        "event_id": event_id,
        "event_type": event.event_type,
        "status": "processing"
    }

@app.get("/api/stats")
def get_statistics(db: Session = Depends(get_db)):
    """
    Get overall statistics
    """
    total_events = db.query(Event).count()
    verified_events = db.query(Event).filter(Event.is_verified == True).count()
    
    events_by_type = {}
    for event_type in ['wildfire', 'flood', 'deforestation', 'drought']:
        count = db.query(Event).filter(Event.event_type == event_type).count()
        events_by_type[event_type] = count
    
    return {
        "total_events": total_events,
        "verified_events": verified_events,
        "verification_rate": round(verified_events / total_events * 100, 2) if total_events > 0 else 0,
        "events_by_type": events_by_type,
        "timestamp": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)