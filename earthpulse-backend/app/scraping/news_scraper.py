import requests
from bs4 import BeautifulSoup
from newspaper import Article
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class NewsEventScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.environmental_keywords = [
            'wildfire', 'forest fire', 'bushfire',
            'flood', 'flooding', 'inundation',
            'deforestation', 'illegal logging', 'forest clearance',
            'drought', 'heatwave', 'cyclone', 'hurricane'
        ]
    
    def scrape_google_news(self, query="wildfire OR flood OR deforestation", max_results=20):
        """Scrape Google News for environmental events"""
        try:
            url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.content, 'xml')
            
            items = soup.find_all('item')[:max_results]
            events = []
            
            for item in items:
                try:
                    article_url = item.link.text if item.link else None
                    if not article_url:
                        continue
                    
                    # Use newspaper3k to extract full article
                    article = Article(article_url)
                    article.download()
                    article.parse()
                    
                    event = {
                        'title': article.title,
                        'description': article.text[:500] if article.text else item.description.text,
                        'url': article_url,
                        'published_at': article.publish_date or datetime.utcnow(),
                        'source': 'google_news',
                        'raw_html': article.html
                    }
                    events.append(event)
                    logger.info(f"Scraped: {event['title']}")
                    
                except Exception as e:
                    logger.error(f"Error scraping article: {e}")
                    continue
            
            return events
            
        except Exception as e:
            logger.error(f"Error scraping Google News: {e}")
            return []
    
    def scrape_bbc_news(self, keyword="climate"):
        """Scrape BBC News"""
        try:
            url = f"https://www.bbc.com/search?q={keyword}"
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            articles = soup.find_all('div', {'class': 'ssrcss-1f3bvyz-Stack'})
            events = []
            
            for article in articles[:10]:
                try:
                    title_elem = article.find('h2')
                    link_elem = article.find('a')
                    
                    if title_elem and link_elem:
                        article_url = 'https://www.bbc.com' + link_elem['href']
                        
                        # Download full article
                        art = Article(article_url)
                        art.download()
                        art.parse()
                        
                        event = {
                            'title': art.title,
                            'description': art.text[:500],
                            'url': article_url,
                            'published_at': art.publish_date or datetime.utcnow(),
                            'source': 'bbc_news'
                        }
                        events.append(event)
                        
                except Exception as e:
                    logger.error(f"Error parsing BBC article: {e}")
                    continue
            
            return events
            
        except Exception as e:
            logger.error(f"Error scraping BBC: {e}")
            return []

# Usage
scraper = NewsEventScraper()
events = scraper.scrape_google_news()