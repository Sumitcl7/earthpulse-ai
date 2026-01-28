import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

# Test events data
test_events = [
    {
        "event_type": "wildfire",
        "title": "California Wildfire Burns 10,000 Acres",
        "description": "A massive wildfire in Northern California has burned over 10,000 acres, forcing thousands to evacuate.",
        "severity": "high",
        "location_name": "California",
        "latitude": 36.7783,
        "longitude": -119.4179,
        "source_url": "https://example.com/wildfire1",
        "source_type": "news",
        "published_at": datetime.now().isoformat()
    },
    {
        "event_type": "flood",
        "title": "Heavy Flooding in Texas",
        "description": "Severe flooding has impacted several communities in Texas after record rainfall.",
        "severity": "medium",
        "location_name": "Texas",
        "latitude": 31.9686,
        "longitude": -99.9018,
        "source_url": "https://example.com/flood1",
        "source_type": "news",
        "published_at": datetime.now().isoformat()
    },
    {
        "event_type": "deforestation",
        "title": "Illegal Logging Discovered in Amazon",
        "description": "Satellite imagery reveals extensive illegal logging activity in the Amazon rainforest.",
        "severity": "critical",
        "location_name": "Amazon Rainforest",
        "latitude": -3.4653,
        "longitude": -62.2159,
        "source_url": "https://example.com/deforestation1",
        "source_type": "satellite",
        "published_at": datetime.now().isoformat()
    },
    {
        "event_type": "wildfire",
        "title": "Australian Bushfire Threatens Wildlife",
        "description": "A bushfire in Australia is threatening critical wildlife habitats.",
        "severity": "high",
        "location_name": "Australia",
        "latitude": -25.2744,
        "longitude": 133.7751,
        "source_url": "https://example.com/wildfire2",
        "source_type": "news",
        "published_at": datetime.now().isoformat()
    },
    {
        "event_type": "drought",
        "title": "Severe Drought Affects East Africa",
        "description": "Prolonged drought conditions continue to impact agriculture in East Africa.",
        "severity": "high",
        "location_name": "Kenya",
        "latitude": -0.0236,
        "longitude": 37.9062,
        "source_url": "https://example.com/drought1",
        "source_type": "news",
        "published_at": datetime.now().isoformat()
    }
]

print("🌍 Adding test events to EarthPulse AI database...\n")

# We need to add events directly to database since we don't have a POST endpoint yet
# Let's create one!

print("⚠️ We need to add a POST endpoint first!")
print("\nCopy this code to your app/main.py to add event creation endpoint:\n")

endpoint_code = '''
@app.post("/api/events/create")
def create_event(
    event_type: str,
    title: str,
    description: str,
    severity: str,
    location_name: str,
    latitude: float,
    longitude: float,
    source_url: str = None,
    source_type: str = "manual",
    db: Session = Depends(get_db)
):
    """
    Manually create an event
    """
    from datetime import datetime
    
    event = Event(
        event_type=event_type,
        title=title,
        description=description,
        severity=severity,
        location_name=location_name,
        latitude=latitude,
        longitude=longitude,
        source_url=source_url,
        source_type=source_type,
        published_at=datetime.utcnow(),
        verification_status='pending'
    )
    
    db.add(event)
    db.commit()
    db.refresh(event)
    
    return {
        "message": "Event created successfully",
        "event_id": event.id
    }
'''

print(endpoint_code)