
import requests
import json
from typing import List, Dict, Optional

class SerpAPIIntegration:
    """Integrazione con SerpAPI per ricerche reali"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://serpapi.com/search"
    
    def search(self, query: str, language: str = 'it', num_results: int = 5) -> List[Dict]:
        """Esegue una ricerca su Google tramite SerpAPI"""
        
        try:
            params = {
                'q': query,
                'api_key': self.api_key,
                'engine': 'google',
                'num': num_results,
                'hl': language,
                'gl': 'it' if language == 'it' else 'us'
            }
            
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            results = []
            if 'organic_results' in data:
                for result in data['organic_results']:
                    results.append({
                        'title': result.get('title', ''),
                        'snippet': result.get('snippet', ''),
                        'link': result.get('link', ''),
                        'source': result.get('source', '')
                    })
            
            return results
            
        except requests.RequestException as e:
            print(f"Errore SerpAPI: {e}")
            return []
        except json.JSONDecodeError as e:
            print(f"Errore parsing JSON: {e}")
            return []
        except Exception as e:
            print(f"Errore generico: {e}")
            return []
    
    def search_news(self, query: str, language: str = 'it', num_results: int = 5) -> List[Dict]:
        """Esegue una ricerca di notizie su Google News"""
        
        try:
            params = {
                'q': query,
                'api_key': self.api_key,
                'engine': 'google_news',
                'num': num_results,
                'hl': language,
                'gl': 'it' if language == 'it' else 'us'
            }
            
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            results = []
            if 'news_results' in data:
                for result in data['news_results']:
                    results.append({
                        'title': result.get('title', ''),
                        'snippet': result.get('snippet', ''),
                        'link': result.get('link', ''),
                        'source': result.get('source', ''),
                        'date': result.get('date', '')
                    })
            
            return results
            
        except requests.RequestException as e:
            print(f"Errore SerpAPI News: {e}")
            return []
        except json.JSONDecodeError as e:
            print(f"Errore parsing JSON: {e}")
            return []
        except Exception as e:
            print(f"Errore generico: {e}")
            return []
    
    def search_official_sources(self, query: str, language: str = 'it') -> List[Dict]:
        """Cerca specificamente su fonti ufficiali"""
        
        official_terms = [
            f'"{query}" site:governo.it',
            f'"{query}" site:parlamento.it',
            f'"{query}" site:quirinale.it',
            f'"{query}" site:istat.it',
            f'"{query}" site:ansa.it',
            f'"{query}" site:repubblica.it',
            f'"{query}" site:corriere.it'
        ]
        
        all_results = []
        
        for official_query in official_terms:
            results = self.search(official_query, language, 3)
            all_results.extend(results)
        
        return all_results[:10]  # Limita a 10 risultati totali

class SearchManager:
    """Gestisce le ricerche per gli agenti specializzati"""
    
    def __init__(self, serpapi_key: Optional[str] = None):
        self.serpapi = None
        if serpapi_key:
            self.serpapi = SerpAPIIntegration(serpapi_key)
    
    def execute_search(self, queries: List[str], search_type: str = 'general', language: str = 'it') -> List[Dict]:
        """Esegue ricerche per le query fornite"""
        
        if not self.serpapi:
            return self._simulate_search(queries)
        
        all_results = []
        
        for query in queries:
            if search_type == 'news':
                results = self.serpapi.search_news(query, language)
            elif search_type == 'official':
                results = self.serpapi.search_official_sources(query, language)
            else:
                results = self.serpapi.search(query, language)
            
            all_results.append({
                'query': query,
                'results': results,
                'search_type': search_type
            })
        
        return all_results
    
    def _simulate_search(self, queries: List[str]) -> List[Dict]:
        """Simula ricerche quando SerpAPI non è disponibile"""
        
        results = []
        
        for query in queries:
            results.append({
                'query': query,
                'results': [
                    {
                        'title': f'Risultato simulato per: {query}',
                        'snippet': 'Questo è un risultato simulato. Per risultati reali, configura SerpAPI.',
                        'link': 'https://example.com',
                        'source': 'Simulato'
                    }
                ],
                'search_type': 'simulated'
            })
        
        return results 