
import requests
import json
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import urllib.parse

class ScrapingDogIntegration:
    """Integrazione con ScrapingDog per ricerche reali"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.scrapingdog.com/google"
    
    def search(self, query: str, language: str = 'it', num_results: int = 5) -> List[Dict]:
        """Esegue una ricerca su Google tramite ScrapingDog"""
        
        try:
            params = {
                'api_key': self.api_key,
                'query': query,
                'num': num_results,
                'hl': language,
                'gl': 'it' if language == 'it' else 'us'
            }
            
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            results = []
            if 'organic_results' in data and data['organic_results']:
                for result in data['organic_results']:
                    results.append({
                        'title': result.get('title', ''),
                        'snippet': result.get('snippet', ''),
                        'link': result.get('link', ''),
                        'source': result.get('source', '')
                    })
            else:
                pass
            
            return results
            
        except requests.RequestException as e:
            return []
        except json.JSONDecodeError as e:
            return []
        except Exception as e:
            return []
    
    def search_news(self, query: str, language: str = 'it', num_results: int = 5) -> List[Dict]:
        """Esegue una ricerca di notizie su Google News"""
        
        try:
            params = {
                'api_key': self.api_key,
                'query': query,
                'num': num_results,
                'hl': language,
                'gl': 'it' if language == 'it' else 'us',
                'tbm': 'nws'  # Google News
            }
            
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            results = []
            if 'news_results' in data and data['news_results']:
                for result in data['news_results']:
                    results.append({
                        'title': result.get('title', ''),
                        'snippet': result.get('snippet', ''),
                        'link': result.get('link', ''),
                        'source': result.get('source', ''),
                        'date': result.get('date', '')
                    })
            elif 'organic_results' in data and data['organic_results']:
                for result in data['organic_results']:
                    results.append({
                        'title': result.get('title', ''),
                        'snippet': result.get('snippet', ''),
                        'link': result.get('link', ''),
                        'source': result.get('source', ''),
                        'date': ''
                    })
            else:
                pass
            
            return results
            
        except requests.RequestException as e:
            return []
        except json.JSONDecodeError as e:
            return []
        except Exception as e:
            return [] 