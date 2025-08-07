
import requests
from bs4 import BeautifulSoup
import re
import time
from urllib.parse import urlparse
from typing import Dict, Optional, List
import random

class ArticleScraper:
    """Scraper intelligente per estrarre contenuto da articoli web"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'it-IT,it;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        self.content_selectors = {
            'ansa.it': [
                '.news-content',
                '.article-content',
                '.content',
                'article',
                '.news-text',
                '.article-body'
            ],
            'repubblica.it': [
                '.entry-content',
                '.article-content',
                '.content',
                'article',
                '.article-body'
            ],
            'corriere.it': [
                '.article-content',
                '.content',
                'article',
                '.article-body',
                '.article-text'
            ],
            'ilsole24ore.com': [
                '.article-content',
                '.content',
                'article',
                '.article-body',
                '.article-text'
            ],
            'sky.it': [
                '.article-content',
                '.content',
                'article',
                '.article-body',
                '.article-text'
            ],
            'rainews.it': [
                '.article-content',
                '.content',
                'article',
                '.article-body',
                '.article-text'
            ],
            'adnkronos.com': [
                '.article-content',
                '.content',
                'article',
                '.article-body',
                '.article-text'
            ],
            'agi.it': [
                '.article-content',
                '.content',
                'article',
                '.article-body',
                '.article-text'
            ],
            'reuters.com': [
                '.article-content',
                '.content',
                'article',
                '.article-body',
                '.article-text'
            ],
            'bbc.com': [
                '.article-content',
                '.content',
                'article',
                '.article-body',
                '.article-text'
            ],
            'default': [
                'article',
                '.article-content',
                '.content',
                '.post-content',
                '.entry-content',
                '.main-content',
                '.story-content',
                '.news-content'
            ]
        }
        
        self.title_selectors = [
            'h1',
            '.article-title',
            '.title',
            '.headline',
            '.news-title',
            'title'
        ]
        
        self.date_selectors = [
            '.article-date',
            '.date',
            '.published-date',
            '.timestamp',
            'time',
            '.article-time'
        ]
        
        self.author_selectors = [
            '.author',
            '.byline',
            '.article-author',
            '.writer',
            '.reporter'
        ]
    
    def extract_domain(self, url: str) -> str:
        """Estrae il dominio da un URL"""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            if domain.startswith('www.'):
                domain = domain[4:]
            return domain
        except:
            return 'default'
    
    def get_content_selectors(self, domain: str) -> List[str]:
        """Ottiene i selettori CSS appropriati per il dominio"""
        for site_domain, selectors in self.content_selectors.items():
            if site_domain in domain:
                return selectors
        return self.content_selectors['default']
    
    def clean_text(self, text: str) -> str:
        """Pulisce il testo estratto"""
        if not text:
            return ""
        
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        text = ansi_escape.sub('', text)
        
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
        
        text = re.sub(r'\s+', ' ', text)
        
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
        text = text.strip()
        
        return text
    
    def extract_title(self, soup: BeautifulSoup) -> str:
        """Estrae il titolo dell'articolo"""
        for selector in self.title_selectors:
            title_elem = soup.select_one(selector)
            if title_elem:
                title = title_elem.get_text(strip=True)
                if title and len(title) > 10:  # Titolo deve essere significativo
                    return title
        
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.get_text(strip=True)
        
        return "Titolo non disponibile"
    
    def extract_date(self, soup: BeautifulSoup) -> str:
        """Estrae la data dell'articolo"""
        for selector in self.date_selectors:
            date_elem = soup.select_one(selector)
            if date_elem:
                date_text = date_elem.get_text(strip=True)
                if date_text:
                    return date_text
        
        time_elem = soup.find('time')
        if time_elem and time_elem.get('datetime'):
            return time_elem.get('datetime')
        
        return "Data non disponibile"
    
    def extract_author(self, soup: BeautifulSoup) -> str:
        """Estrae l'autore dell'articolo"""
        for selector in self.author_selectors:
            author_elem = soup.select_one(selector)
            if author_elem:
                author = author_elem.get_text(strip=True)
                if author and len(author) > 2:
                    return author
        
        return "Autore non disponibile"
    
    def extract_content(self, soup: BeautifulSoup, domain: str) -> str:
        """Estrae il contenuto principale dell'articolo"""
        content_selectors = self.get_content_selectors(domain)
        
        for selector in content_selectors:
            content_elem = soup.select_one(selector)
            if content_elem:
                unwanted_selectors = [
                    'script', 'style', 'nav', 'header', 'footer', 
                    '.advertisement', '.ads', '.social-share', '.related-articles',
                    '.sidebar', '.comments', '.recommendations', '.newsletter',
                    '.breadcrumb', '.navigation', '.menu', '.footer',
                    '.header', '.top-bar', '.bottom-bar', '.social-media',
                    '.share-buttons', '.tags', '.categories', '.author-bio',
                    '.related-content', '.more-articles', '.trending',
                    '.popular', '.latest', '.breaking', '.featured'
                ]
                
                for unwanted_selector in unwanted_selectors:
                    for unwanted in content_elem.select(unwanted_selector):
                        unwanted.decompose()
                
                content = content_elem.get_text()
                content = self.clean_text(content)
                
                if content and len(content) > 100:  # Contenuto deve essere significativo
                    return content
        
        paragraphs = soup.find_all('p')
        if paragraphs:
            content_parts = []
            for p in paragraphs:
                parent = p.parent
                is_main_content = False
                
                if parent and parent.get('class'):
                    parent_classes = ' '.join(parent.get('class')).lower()
                    main_content_indicators = ['article', 'content', 'main', 'story', 'news']
                    if any(indicator in parent_classes for indicator in main_content_indicators):
                        is_main_content = True
                
                text = p.get_text(strip=True)
                if (text and len(text) > 30 and 
                    not any(nav_word in text.lower() for nav_word in ['home', 'menu', 'search', 'login', 'register', 'cookie', 'privacy'])):
                    content_parts.append(text)
            
            if content_parts:
                return '\n\n'.join(content_parts)
        
        return "Contenuto non disponibile"
    
    def scrape_article(self, url: str) -> Optional[Dict]:
        """Scarica e analizza un articolo da un URL"""
        try:
            print(f"🔍 Scraping: {url}")
            
            time.sleep(random.uniform(1, 3))
            
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            if 'text/html' not in response.headers.get('content-type', ''):
                print("❌ La pagina non è HTML")
                return None
            
            soup = BeautifulSoup(response.content, 'html.parser')
            domain = self.extract_domain(url)
            
            title = self.extract_title(soup)
            content = self.extract_content(soup, domain)
            date = self.extract_date(soup)
            author = self.extract_author(soup)
            
            if not content or content == "Contenuto non disponibile" or len(content) < 100:
                print("❌ Contenuto insufficiente o non trovato")
                return None
            
            article = {
                'title': title,
                'content': content,
                'summary': content[:500] + "..." if len(content) > 500 else content,
                'date': date,
                'author': author,
                'source': domain,
                'link': url,
                'scraped': True
            }
            
            print(f"✅ Articolo estratto: {len(content)} caratteri")
            print(f"📰 Titolo: {title}")
            print(f"📅 Data: {date}")
            print(f"✍️ Autore: {author}")
            print(f"🌐 Fonte: {domain}")
            return article
            
        except requests.RequestException as e:
            print(f"❌ Errore di rete: {e}")
            return None
        except Exception as e:
            print(f"❌ Errore durante lo scraping: {e}")
            return None
    
    def validate_url(self, url: str) -> bool:
        """Valida se l'URL sembra essere un articolo di notizia"""
        if not url or not url.startswith(('http://', 'https://')):
            return False
        
        url_lower = url.lower()
        article_keywords = [
            'article', 'news', 'story', 'post', 'blog',
            'articolo', 'notizia', 'storia', 'cronaca',
            'politica', 'economia', 'sport', 'cultura',
            'ansa', 'repubblica', 'corriere', 'sole24ore',
            'sky', 'rai', 'adnkronos', 'agi', 'reuters', 'bbc'
        ]
        
        if any(keyword in url_lower for keyword in article_keywords):
            return True
        
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            return bool(parsed.netloc and parsed.path)
        except:
            return False
    
    def get_article_info(self, url: str) -> Optional[Dict]:
        """Ottiene informazioni rapide sull'articolo senza scaricare tutto"""
        try:
            response = self.session.head(url, timeout=10)
            response.raise_for_status()
            
            return {
                'url': url,
                'status': response.status_code,
                'content_type': response.headers.get('content-type', ''),
                'content_length': response.headers.get('content-length', '0'),
                'is_html': 'text/html' in response.headers.get('content-type', '')
            }
        except:
            return None 