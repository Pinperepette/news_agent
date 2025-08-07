
import requests
from xml.etree import ElementTree as ET
import re
import html
from datetime import datetime
import time

def fetch_articles(feed_url, user_agent="Mozilla/5.0"):
    res = requests.get(feed_url, timeout=10, headers={"User-Agent": user_agent})
    res.raise_for_status()
    root = ET.fromstring(res.text)
    articles = []
    for item in root.findall('.//item'):
        title = item.findtext('title', '')
        link = item.findtext('link', '')
        pubDate = item.findtext('pubDate', '')
        description = item.findtext('description', '')
        source_el = item.find('source')
        author = source_el.text if source_el is not None else ""
        
        clean_descr = re.sub('<[^<]+?>', '', description)
        clean_descr = html.unescape(clean_descr)
        clean_descr = re.sub(r'&[a-zA-Z0-9#]+;', '', clean_descr)
        clean_descr = re.sub(r'\s+', ' ', clean_descr)
        
        clean_title = html.unescape(title)
        clean_title = re.sub(r'&[a-zA-Z0-9#]+;', '', clean_title)
        clean_title = re.sub(r'\s+', ' ', clean_title)
        
        clean_author = html.unescape(author)
        clean_author = re.sub(r'&[a-zA-Z0-9#]+;', '', clean_author)
        clean_author = re.sub(r'\s+', ' ', clean_author)
        
        articles.append({
            "title": clean_title.strip(),
            "date": pubDate.strip(),
            "author": clean_author.strip(),
            "summary": clean_descr.strip(),
            "link": link.strip(),
            "source": extract_source_from_url(link.strip()),
            "parsed_date": parse_date(pubDate.strip())
        })
    return articles

def fetch_multiple_sources(sources=None, max_articles_per_source=10):
    """Recupera articoli da multiple fonti"""
    
    if sources is None:
        sources = [
            'https://www.ansa.it/sito/ansait_rss.xml',
            'https://www.repubblica.it/rss/homepage/rss2.0.xml',
            'https://www.corriere.it/rss/homepage.xml',
            'https://www.ilsole24ore.com/rss/homepage.xml',
            'https://feeds.reuters.com/reuters/topNews',
            'https://feeds.bbci.co.uk/news/rss.xml'
        ]
    
    all_articles = []
    
    for source_url in sources:
        try:
            source_name = extract_source_from_url(source_url)
            print(f"📰 Recuperando da: {source_name}")
            articles = fetch_articles(source_url)
            if articles:
                all_articles.extend(articles[:max_articles_per_source])
                print(f"   ✅ {len(articles[:max_articles_per_source])} articoli recuperati")
            else:
                print(f"   ⚠️ Nessun articolo trovato")
            time.sleep(1)  # Pausa per non sovraccaricare i server
        except Exception:
            source_name = extract_source_from_url(source_url)
            print(f"   ⚠️ {source_name}: non disponibile")
            continue  # Continua con la prossima fonte
    
    if all_articles:
        all_articles.sort(key=lambda x: x.get('parsed_date', ''), reverse=True)
        print(f"✅ Caricamento completato: {len(all_articles)} articoli da {len(set(article.get('source', '') for article in all_articles))} fonti")
    else:
        print("⚠️ Nessun articolo disponibile al momento")
    
    return all_articles

def extract_source_from_url(url):
    """Estrae il nome della fonte dall'URL"""
    if not url:
        return "Sconosciuto"
    
    source_map = {
        'ansa.it': 'ANSA',
        'repubblica.it': 'La Repubblica',
        'corriere.it': 'Corriere della Sera',
        'ilsole24ore.com': 'Il Sole 24 Ore',
        'reuters.com': 'Reuters',
        'bbc.co.uk': 'BBC News',
        'adnkronos.com': 'Adnkronos',
        'agi.it': 'AGI'
    }
    
    for domain, name in source_map.items():
        if domain in url:
            return name
    
    try:
        from urllib.parse import urlparse
        domain = urlparse(url).netloc
        return domain.replace('www.', '')
    except:
        return "Sconosciuto"

def parse_date(date_string):
    """Converte la data in formato standard"""
    if not date_string:
        return ''
    
    try:
        formats = [
            '%a, %d %b %Y %H:%M:%S %z',
            '%a, %d %b %Y %H:%M:%S',
            '%Y-%m-%dT%H:%M:%S%z',
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%d'
        ]
        
        for fmt in formats:
            try:
                parsed_date = datetime.strptime(date_string, fmt)
                return parsed_date.strftime('%Y-%m-%d')
            except ValueError:
                continue
        
        return ''
        
    except Exception:
        return ''
