# app/main.py - COMPLETE CORRECTED VERSION
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
import logging

from app.database import engine, Base, get_db
from app.models.event import Event
from app.services.earth_engine import earth_engine_service
from app.services.news_scraper import scrape_environmental_news
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.models.user import User
from app.services.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_active_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s:%(name)s:%(message)s'
)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)
logger.info("✅ Database initialized successfully")

# Initialize FastAPI app
app = FastAPI(
    title="EarthPulse AI API",
    description="Environmental event monitoring with satellite analysis",
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


# ==================== ROOT & HEALTH ====================

@app.get("/")
async def root():
    return {
        "message": "🌍 EarthPulse AI API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "events": "/api/events",
            "stats": "/api/stats",
            "satellite": "/api/satellite/*",
            "news": "/api/news/scrape"
        }
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "earth_engine": "active" if earth_engine_service.initialized else "inactive",
        "timestamp": datetime.utcnow().isoformat()
    }


# ==================== AUTHENTICATION ====================

@app.post("/api/auth/register")
async def register(
    email: str,
    username: str,
    password: str,
    full_name: str = None,
    db: Session = Depends(get_db)
):
    # Check if user exists
    existing_user = db.query(User).filter(
        (User.email == email) | (User.username == username)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email or username already registered"
        )
    
    # Create new user
    user = User(
        email=email,
        username=username,
        hashed_password=get_password_hash(password),
        full_name=full_name,
        saved_locations=[],
        preferences={}
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    logger.info(f"✅ New user registered: {username}")
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "full_name": user.full_name
        }
    }


@app.post("/api/auth/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Find user by email or username
    user = db.query(User).filter(
        (User.email == form_data.username) | (User.username == form_data.username)
    ).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email/username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    logger.info(f"✅ User logged in: {user.username}")
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "full_name": user.full_name
        }
    }


@app.get("/api/auth/me")
async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username,
        "full_name": current_user.full_name,
        "saved_locations": current_user.saved_locations,
        "preferences": current_user.preferences,
        "created_at": current_user.created_at.isoformat()
    }


@app.post("/api/auth/save-location")
async def save_location(
    location_name: str,
    latitude: float,
    longitude: float,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    saved_locations = current_user.saved_locations or []
    
    new_location = {
        "name": location_name,
        "latitude": latitude,
        "longitude": longitude,
        "saved_at": datetime.utcnow().isoformat()
    }
    
    saved_locations.append(new_location)
    current_user.saved_locations = saved_locations
    
    db.commit()
    db.refresh(current_user)
    
    return {"message": "Location saved", "saved_locations": saved_locations}


# ==================== STATISTICS ====================

@app.get("/api/stats")
async def get_statistics(db: Session = Depends(get_db)):
    total_events = db.query(Event).count()
    verified_events = db.query(Event).filter(Event.is_verified == True).count()
    
    events_by_type = {
        'wildfire': db.query(Event).filter(Event.event_type == 'wildfire').count(),
        'flood': db.query(Event).filter(Event.event_type == 'flood').count(),
        'deforestation': db.query(Event).filter(Event.event_type == 'deforestation').count(),
        'drought': db.query(Event).filter(Event.event_type == 'drought').count(),
    }
    
    verification_rate = round((verified_events / total_events * 100) if total_events > 0 else 0, 1)
    
    return {
        "total_events": total_events,
        "verified_events": verified_events,
        "verification_rate": verification_rate,
        "events_by_type": events_by_type,
        "timestamp": datetime.utcnow().isoformat()
    }


# ==================== EVENTS ====================

@app.get("/api/events")
async def get_events(
    event_type: str = None,
    severity: str = None,
    verified_only: bool = False,
    db: Session = Depends(get_db)
):
    query = db.query(Event)
    
    if event_type:
        query = query.filter(Event.event_type == event_type)
    if severity:
        query = query.filter(Event.severity == severity)
    if verified_only:
        query = query.filter(Event.is_verified == True)
    
    events = query.order_by(Event.created_at.desc()).all()
    
    return [
        {
            "id": event.id,
            "event_type": event.event_type,
            "title": event.title,
            "description": event.description,
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
            "verification_score": event.verification_score,
            "created_at": event.created_at.isoformat() if event.created_at else None,
        }
        for event in events
    ]


@app.get("/api/events/{event_id}")
async def get_event(event_id: int, db: Session = Depends(get_db)):
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
            "latitude": event.latitude,
            "longitude": event.longitude
        },
        "source_url": event.source_url,
        "published_at": event.published_at.isoformat() if event.published_at else None,
        "is_verified": event.is_verified,
        "verification_status": event.verification_status,
        "verification_score": event.verification_score,
        "analysis_results": event.analysis_results,
        "created_at": event.created_at.isoformat() if event.created_at else None,
        "updated_at": event.updated_at.isoformat() if event.updated_at else None,
    }


@app.post("/api/events/create")
async def create_event(
    event_type: str,
    title: str,
    description: str,
    severity: str,
    location_name: str,
    latitude: float,
    longitude: float,
    source_url: str = None,
    db: Session = Depends(get_db)
):
    event = Event(
        event_type=event_type,
        title=title,
        description=description,
        severity=severity,
        location_name=location_name,
        latitude=latitude,
        longitude=longitude,
        source_url=source_url,
        source_type="manual",
        published_at=datetime.utcnow()
    )
    
    db.add(event)
    db.commit()
    db.refresh(event)
    
    logger.info(f"✅ Created event: {event.title}")
    
    return {"message": "Event created", "event_id": event.id}


@app.post("/api/events/{event_id}/verify")
async def verify_event_with_satellite(
    event_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    event = db.query(Event).filter(Event.id == event_id).first()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    def verify():
        # Create a new database session for the background task
        from app.database import SessionLocal
        db_task = SessionLocal()
        
        try:
            # Get fresh event object in this session
            event = db_task.query(Event).filter(Event.id == event_id).first()
            
            if not event:
                logger.error(f"Event {event_id} not found in background task")
                return
            
            logger.info(f"🔍 Verifying event {event_id}: {event.title}")
            
            result = None
            verified = False
            score = 0.5
            
            lat = event.latitude
            lon = event.longitude
            
            if event.event_type == 'wildfire':
                result = earth_engine_service.detect_wildfires(lat, lon, radius_km=50)
                if result and "error" not in result:
                    verified = result.get('fire_detected', False)
                    score = 0.9 if verified else 0.2
                    
            elif event.event_type == 'flood':
                result = earth_engine_service.detect_water_changes(lat, lon, radius_km=20)
                if result and "error" not in result:
                    verified = result.get('water_present', False)
                    score = 0.8 if verified else 0.3
                    
            elif event.event_type == 'deforestation':
                result = earth_engine_service.get_ndvi(lat, lon, radius_km=10)
                if result and "error" not in result:
                    ndvi = result.get('ndvi_mean')
                    if ndvi is not None:
                        verified = ndvi < 0.3
                        score = 0.85 if verified else 0.25
                        
            elif event.event_type == 'drought':
                result = earth_engine_service.detect_water_changes(lat, lon, radius_km=20)
                if result and "error" not in result:
                    ndwi = result.get('ndwi_mean')
                    if ndwi is not None:
                        verified = ndwi < 0.0
                        score = 0.8 if verified else 0.3
            
            # Update event
            event.is_verified = verified
            event.verification_score = score
            event.verification_status = 'verified' if verified else 'unverified'
            event.verification_method = 'satellite'
            event.analysis_results = result
            event.updated_at = datetime.utcnow()
            
            db_task.commit()
            db_task.refresh(event)
            
            logger.info(f"✅ Event {event_id} verified: {verified} (score: {score})")
            
        except Exception as e:
            logger.error(f"❌ Error verifying event {event_id}: {e}")
            db_task.rollback()
        finally:
            db_task.close()
    
    background_tasks.add_task(verify)
    
    return {
        "message": "Verification started",
        "event_id": event_id,
        "status": "processing"
    }


# ==================== SATELLITE ANALYSIS ====================

@app.get("/api/satellite/ndvi")
async def get_ndvi(latitude: float, longitude: float, radius_km: float = 10):
    try:
        result = earth_engine_service.get_ndvi(latitude, longitude, radius_km=radius_km)
        return result
    except Exception as e:
        logger.error(f"Error in NDVI analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/satellite/wildfire")
async def detect_wildfire(latitude: float, longitude: float, radius_km: float = 50):
    try:
        result = earth_engine_service.detect_wildfires(latitude, longitude, radius_km=radius_km)
        return result
    except Exception as e:
        logger.error(f"Error in wildfire detection: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/satellite/water")
async def detect_water(latitude: float, longitude: float, radius_km: float = 20):
    try:
        result = earth_engine_service.detect_water_changes(latitude, longitude, radius_km=radius_km)
        return result
    except Exception as e:
        logger.error(f"Error in water detection: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== NEWS SCRAPING ====================

@app.get("/api/news/scrape")
async def scrape_news(query: str = "wildfire OR flood OR deforestation", max_results: int = 20):
    try:
        news_items = scrape_environmental_news(query, max_results)
        return {
            "count": len(news_items),
            "news": news_items,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error scraping news: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/news/import/{news_index}")
async def import_news_as_event(news_index: int, db: Session = Depends(get_db)):
    try:
        news_items = scrape_environmental_news()
        
        if news_index >= len(news_items):
            raise HTTPException(status_code=404, detail="News item not found")
        
        news_item = news_items[news_index]
        
        event = Event(
            event_type=news_item.get('event_type', 'wildfire'),
            title=news_item['title'],
            description=news_item['description'],
            severity='medium',
            location_name=news_item['location']['name'],
            latitude=news_item['location']['latitude'],
            longitude=news_item['location']['longitude'],
            source_url=news_item['url'],
            source_type='news_scraper',
            published_at=datetime.utcnow()
        )
        
        db.add(event)
        db.commit()
        db.refresh(event)
        
        logger.info(f"✅ Imported news as event: {event.title}")
        
        return {"message": "News imported as event", "event_id": event.id}
        
    except Exception as e:
        logger.error(f"Error importing news: {e}")
        raise HTTPException(status_code=500, detail=str(e))