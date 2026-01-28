import spacy
from transformers import pipeline
from geopy.geocoders import Nominatim
import logging

logger = logging.getLogger(__name__)

class EventExtractor:
    def __init__(self):
        # Load spaCy model for NER
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            logger.warning("Downloading spaCy model...")
            import os
            os.system("python -m spacy download en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")
        
        # Transformers for event classification
        self.classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        
        # Geocoder for location coordinates
        self.geocoder = Nominatim(user_agent="earthpulse_ai")
        
        self.event_types = ["wildfire", "flood", "deforestation", "drought", "earthquake", "hurricane"]
    
    def extract_locations(self, text):
        """Extract location entities from text"""
        doc = self.nlp(text)
        locations = []
        
        for ent in doc.ents:
            if ent.label_ in ["GPE", "LOC", "FAC"]:  # Geopolitical Entity, Location, Facility
                locations.append({
                    'name': ent.text,
                    'type': ent.label_
                })
        
        return locations
    
    def geocode_location(self, location_name):
        """Convert location name to lat/lon coordinates"""
        try:
            location = self.geocoder.geocode(location_name)
            if location:
                return {
                    'name': location_name,
                    'latitude': location.latitude,
                    'longitude': location.longitude,
                    'full_address': location.address
                }
        except Exception as e:
            logger.error(f"Geocoding error for {location_name}: {e}")
        
        return None
    
    def classify_event_type(self, text):
        """Classify the type of environmental event"""
        try:
            result = self.classifier(text, self.event_types)
            return {
                'event_type': result['labels'][0],
                'confidence': result['scores'][0]
            }
        except Exception as e:
            logger.error(f"Classification error: {e}")
            return {'event_type': 'unknown', 'confidence': 0.0}
    
    def process_article(self, article_data):
        """Process article to extract structured event information"""
        text = f"{article_data['title']} {article_data['description']}"
        
        # Extract locations
        locations = self.extract_locations(text)
        
        # Geocode first location
        geo_data = None
        if locations:
            geo_data = self.geocode_location(locations[0]['name'])
        
        # Classify event type
        event_classification = self.classify_event_type(text)
        
        return {
            **article_data,
            'locations': locations,
            'primary_location': geo_data,
            'event_type': event_classification['event_type'],
            'event_confidence': event_classification['confidence']
        }

# Usage
extractor = EventExtractor()
processed_event = extractor.process_article({
    'title': 'Massive wildfire in California',
    'description': 'A large wildfire is burning near Los Angeles...'
})