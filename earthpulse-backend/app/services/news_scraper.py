# app/services/news_scraper.py
import logging
import requests
from datetime import datetime, timedelta
from typing import List, Dict
import random

logger = logging.getLogger(__name__)

def scrape_environmental_news(query: str = "wildfire OR flood OR deforestation", max_results: int = 20) -> List[Dict]:
    """
    Scrape environmental news - returns mock data for demo
    In production, connect to news APIs like NewsAPI, GDELT, etc.
    """
    logger.info(f"📰 Scraping news for: {query}")
    
    # Mock news data for demo
    mock_news = [
        {
            'title': 'Massive Wildfire Engulfs California Forest',
            'description': 'A rapidly spreading wildfire has forced thousands to evacuate as it threatens residential areas in Northern California.',
            'url': 'https://example.com/news/wildfire-california',
            'published_at': (datetime.now() - timedelta(hours=2)).isoformat(),
            'source': 'Environmental News Network',
            'event_type': 'wildfire',
            'location': {'name': 'California', 'latitude': 38.5816, 'longitude': -121.4944}
        },
        {
            'title': 'Severe Flooding Hits Southeast Asia',
            'description': 'Monsoon rains cause widespread flooding across Thailand and Vietnam, affecting millions.',
            'url': 'https://example.com/news/flood-asia',
            'published_at': (datetime.now() - timedelta(hours=5)).isoformat(),
            'source': 'Climate Watch',
            'event_type': 'flood',
            'location': {'name': 'Thailand', 'latitude': 15.8700, 'longitude': 100.9925}
        },
        {
            'title': 'Amazon Deforestation Reaches Record High',
            'description': 'Satellite imagery reveals alarming increase in illegal logging and forest clearance in Brazilian Amazon.',
            'url': 'https://example.com/news/amazon-deforestation',
            'published_at': (datetime.now() - timedelta(hours=8)).isoformat(),
            'source': 'Forest Guardian',
            'event_type': 'deforestation',
            'location': {'name': 'Brazilian Amazon', 'latitude': -3.4653, 'longitude': -62.2159}
        },
        {
            'title': 'Record Drought Devastates East African Crops',
            'description': 'Prolonged drought conditions threaten food security across Kenya, Somalia, and Ethiopia.',
            'url': 'https://example.com/news/drought-africa',
            'published_at': (datetime.now() - timedelta(hours=12)).isoformat(),
            'source': 'Climate Crisis Daily',
            'event_type': 'drought',
            'location': {'name': 'Kenya', 'latitude': -0.0236, 'longitude': 37.9062}
        },
        {
            'title': 'Australian Bushfires Threaten Wildlife Reserves',
            'description': 'Extreme heat and dry conditions fuel massive bushfires across New South Wales.',
            'url': 'https://example.com/news/australia-bushfire',
            'published_at': (datetime.now() - timedelta(hours=15)).isoformat(),
            'source': 'Global Environmental Monitor',
            'event_type': 'wildfire',
            'location': {'name': 'New South Wales, Australia', 'latitude': -33.8688, 'longitude': 151.2093}
        },
        {
            'title': 'Mississippi River Flooding Forces Evacuations',
            'description': 'Heavy rainfall causes Mississippi River to overflow, threatening homes and infrastructure.',
            'url': 'https://example.com/news/mississippi-flood',
            'published_at': (datetime.now() - timedelta(days=1)).isoformat(),
            'source': 'US Climate News',
            'event_type': 'flood',
            'location': {'name': 'Mississippi, USA', 'latitude': 32.3547, 'longitude': -89.3985}
        },
        {
            'title': 'Indonesian Rainforest Cleared for Palm Oil',
            'description': 'Environmentalists raise alarm over rapid deforestation in Borneo for agricultural expansion.',
            'url': 'https://example.com/news/indonesia-deforestation',
            'published_at': (datetime.now() - timedelta(days=1, hours=3)).isoformat(),
            'source': 'Rainforest Alliance',
            'event_type': 'deforestation',
            'location': {'name': 'Borneo, Indonesia', 'latitude': 0.9619, 'longitude': 114.5548}
        },
        {
            'title': 'European Heat Wave Triggers Drought Warnings',
            'description': 'Southern Europe faces severe water shortages as temperatures soar above 40°C.',
            'url': 'https://example.com/news/europe-drought',
            'published_at': (datetime.now() - timedelta(days=2)).isoformat(),
            'source': 'Euro Climate Watch',
            'event_type': 'drought',
            'location': {'name': 'Southern Spain', 'latitude': 37.3891, 'longitude': -5.9845}
        },
    ]
    
    # Filter based on query keywords
    filtered_news = []
    query_lower = query.lower()
    
    for news_item in mock_news:
        if any(keyword in query_lower for keyword in ['wildfire', 'fire', 'burn']) and news_item['event_type'] == 'wildfire':
            filtered_news.append(news_item)
        elif any(keyword in query_lower for keyword in ['flood', 'water', 'rain']) and news_item['event_type'] == 'flood':
            filtered_news.append(news_item)
        elif any(keyword in query_lower for keyword in ['deforestation', 'forest', 'logging']) and news_item['event_type'] == 'deforestation':
            filtered_news.append(news_item)
        elif any(keyword in query_lower for keyword in ['drought', 'dry', 'water shortage']) and news_item['event_type'] == 'drought':
            filtered_news.append(news_item)
        elif 'or' in query_lower.split():
            filtered_news.append(news_item)
    
    # If no specific filter, return all
    if not filtered_news:
        filtered_news = mock_news
    
    result = filtered_news[:max_results]
    logger.info(f"✅ Found {len(result)} news articles")
    
    return result


def create_event_from_news(news_item: Dict) -> Dict:
    """
    Convert news item to event format
    """
    return {
        'event_type': news_item.get('event_type', 'wildfire'),
        'title': news_item['title'],
        'description': news_item['description'],
        'severity': 'medium',
        'location': news_item['location'],
        'source_url': news_item['url'],
        'source_type': 'news_scraper'
    }