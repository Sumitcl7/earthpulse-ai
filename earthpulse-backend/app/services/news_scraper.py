# app/services/news_scraper.py
import requests
from bs4 import BeautifulSoup
from newspaper import Article
from datetime import datetime
import logging
from typing import List, Dict
import spacy
from geopy.geocoders import Nominatim

logger = logging.getLogger(__name__)

class NewsScraperService:
    def __init__(self):
        # Load spaCy model for NER
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            logger.warning("spaCy model not found, downloading...")
            import os
            os.system("python -m spacy download en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")
        
        self.geocoder = Nominatim(user_agent="earthpulse_ai")
        
        self.event_keywords = {
            'wildfire': ['wildfire', 'forest fire', 'bushfire', 'blaze', 'inferno'],
            'flood': ['flood', 'flooding', 'deluge', 'inundation'],
            'deforestation': ['deforestation', 'illegal logging', 'forest clearance', 'tree felling'],
            'drought': ['drought', 'water shortage', 'arid'],
            'earthquake': ['earthquake', 'seismic', 'tremor', 'quake'],
            'hurricane': ['hurricane', 'cyclone', 'typhoon', 'storm']
        }
    
    def scrape_google_news(self, query: str = "wildfire OR flood OR deforestation", 
                          max_results: int = 20) -> List[Dict]:
        """Scrape environmental news from Google News RSS"""
        articles = []
        
        try:
            url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'xml')
            
            items = soup.find_all('item')[:max_results]
            logger.info(f"Found {len(items)} news items")
            
            for item in items:
                try:
                    article_url = item.link.text if item.link else None
                    if not article_url:
                        continue
                    
                    # Parse article
                    article = Article(article_url)
                    article.download()
                    article.parse()
                    
                    # Extract event information
                    event_data = self.extract_event_info(article.title, article.text)
                    
                    articles.append({
                        'title': article.title,
                        'description': article.text[:500] if article.text else '',
                        'url': article_url,
                        'published_at': article.publish_date or datetime.utcnow(),
                        'source': 'google_news',
                        'event_type': event_data['event_type'],
                        'locations': event_data['locations'],
                        'severity': event_data['severity']
                    })
                    
                except Exception as e:
                    logger.error(f"Error parsing article: {e}")
                    continue
            
            logger.info(f"Successfully scraped {len(articles)} articles")
            return articles
            
        except Exception as e:
            logger.error(f"Error scraping Google News: {e}")
            return []
    
    def extract_event_info(self, title: str, text: str) -> Dict:
        """Extract event type, locations, and severity from article"""
        full_text = f"{title} {text}"
        
        # Detect event type
        event_type = self._detect_event_type(full_text)
        
        # Extract locations using NER
        locations = self._extract_locations(full_text)
        
        # Assess severity
        severity = self._assess_severity(full_text)
        
        return {
            'event_type': event_type,
            'locations': locations,
            'severity': severity
        }
    
    def _detect_event_type(self, text: str) -> str:
        """Detect the type of environmental event"""
        text_lower = text.lower()
        
        for event_type, keywords in self.event_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return event_type
        
        return 'unknown'
    
    def _extract_locations(self, text: str) -> List[Dict]:
        """Extract location entities using spaCy NER"""
        doc = self.nlp(text)
        locations = []
        
        for ent in doc.ents:
            if ent.label_ in ["GPE", "LOC"]:  # Geopolitical Entity or Location
                # Try to geocode
                geo_data = self._geocode_location(ent.text)
                if geo_data:
                    locations.append(geo_data)
        
        return locations
    
    def _geocode_location(self, location_name: str) -> Dict:
        """Convert location name to coordinates"""
        try:
            location = self.geocoder.geocode(location_name)
            if location:
                return {
                    'name': location_name,
                    'latitude': location.latitude,
                    'longitude': location.longitude,
                    'address': location.address
                }
        except Exception as e:
            logger.error(f"Geocoding error for {location_name}: {e}")
        
        return None
    
    def _assess_severity(self, text: str) -> str:
        """Assess severity of the event based on keywords"""
        text_lower = text.lower()
        
        critical_keywords = ['catastrophic', 'devastating', 'massive', 'unprecedented', 'disaster']
        high_keywords = ['severe', 'major', 'significant', 'extensive', 'widespread']
        medium_keywords = ['moderate', 'considerable', 'notable']
        
        for keyword in critical_keywords:
            if keyword in text_lower:
                return 'critical'
        
        for keyword in high_keywords:
            if keyword in text_lower:
                return 'high'
        
        for keyword in medium_keywords:
            if keyword in text_lower:
                return 'medium'
        
        return 'low'


# Create singleton instance
news_scraper_service = NewsScraperService()