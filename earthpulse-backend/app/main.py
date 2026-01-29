from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
import logging

from app.database import engine, Base, get_db
from app.models.event import Event

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)
logger.info('✅ Database initialized successfully')

# Initialize FastAPI
app = FastAPI(
    title='EarthPulse AI API',
    description='Environmental Event Monitoring System',
    version='1.0.0'
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/')
async def root():
    return {
        'message': 'EarthPulse AI API',
        'version': '1.0.0',
        'status': 'running'
    }

@app.get('/health')
async def health_check():
    return {
        'status': 'healthy',
        'database': 'connected',
        'timestamp': datetime.utcnow().isoformat()
    }

# ==================== STATISTICS ====================

@app.get('/api/stats')
async def get_statistics(db: Session = Depends(get_db)):
    total_events = db.query(Event).count()
    verified_events = db.query(Event).filter(Event.is_verified == True).count()
    
    events_by_type = {
        'wildfire': db.query(Event).filter(Event.event_type == 'wildfire').count(),
        'flood': db.query(Event).filter(Event.event_type == 'flood').count(),
        'deforestation': db.query(Event).filter(Event.event_type == 'deforestation').count(),
        'drought': db.query(Event).filter(Event.event_type == 'drought').count(),
    }
    
    events_by_severity = {
        'critical': db.query(Event).filter(Event.severity == 'critical').count(),
        'high': db.query(Event).filter(Event.severity == 'high').count(),
        'medium': db.query(Event).filter(Event.severity == 'medium').count(),
        'low': db.query(Event).filter(Event.severity == 'low').count(),
    }
    
    return {
        'total_events': total_events,
        'verified_events': verified_events,
        'unverified_events': total_events - verified_events,
        'events_by_type': events_by_type,
        'events_by_severity': events_by_severity
    }

# ==================== EVENTS ====================

@app.get('/api/events')
async def get_events(
    event_type: str = None,
    severity: str = None,
    verified: bool = None,
    db: Session = Depends(get_db)
):
    query = db.query(Event)
    
    if event_type:
        query = query.filter(Event.event_type == event_type)
    if severity:
        query = query.filter(Event.severity == severity)
    if verified is not None:
        query = query.filter(Event.is_verified == verified)
    
    events = query.order_by(Event.created_at.desc()).all()
    
    return [
        {
            'id': e.id,
            'title': e.title,
            'description': e.description,
            'event_type': e.event_type,
            'severity': e.severity,
            'location': {
                'name': e.location_name,
                'latitude': e.latitude,
                'longitude': e.longitude
            },
            'is_verified': e.is_verified,
            'verification_score': e.verification_score,
            'created_at': e.created_at.isoformat() if e.created_at else None,
            'updated_at': e.updated_at.isoformat() if e.updated_at else None
        }
        for e in events
    ]

@app.get('/api/events/{event_id}')
async def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    
    if not event:
        raise HTTPException(status_code=404, detail='Event not found')
    
    return {
        'id': event.id,
        'title': event.title,
        'description': event.description,
        'event_type': event.event_type,
        'severity': event.severity,
        'location': {
            'name': event.location_name,
            'latitude': event.latitude,
            'longitude': event.longitude
        },
        'is_verified': event.is_verified,
        'verification_score': event.verification_score,
        'created_at': event.created_at.isoformat() if event.created_at else None,
        'updated_at': event.updated_at.isoformat() if event.updated_at else None
    }

@app.post('/api/events/create')
async def create_event(
    title: str,
    description: str,
    event_type: str,
    severity: str,
    location_name: str,
    latitude: float,
    longitude: float,
    db: Session = Depends(get_db)
):
    event = Event(
        title=title,
        description=description,
        event_type=event_type,
        severity=severity,
        location_name=location_name,
        latitude=latitude,
        longitude=longitude,
        is_verified=False
    )
    
    db.add(event)
    db.commit()
    db.refresh(event)
    
    logger.info(f'✅ Created event: {title}')
    
    return {'message': 'Event created', 'event_id': event.id}
