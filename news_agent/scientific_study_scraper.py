
import requests
import time
import random
from urllib.parse import urlparse, quote
from bs4 import BeautifulSoup
import re
import json

class ScientificStudyScraper:
    """Scraper specializzato per studi scientifici e paper"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        
        self.scientific_journals = {
            'archaeometry': 'https://onlinelibrary.wiley.com/journal/14754754',
            'nature': 'https://www.nature.com',
            'science': 'https://www.science.org',
            'pubmed': 'https://pubmed.ncbi.nlm.nih.gov',
            'arxiv': 'https://arxiv.org',
            'researchgate': 'https://www.researchgate.net',
            'academia': 'https://www.academia.edu',
            'scholar': 'https://scholar.google.com',
            'sciencedirect': 'https://www.sciencedirect.com',
            'springer': 'https://link.springer.com',
            'wiley': 'https://onlinelibrary.wiley.com',
            'taylor': 'https://www.tandfonline.com',
            'sage': 'https://journals.sagepub.com'
        }
    
    def find_study_urls(self, study_name, author_name=None):
        """Trova URL di studi scientifici basati su nome e autore"""
        urls = []
        
        scholar_query = f'"{study_name}"'
        if author_name:
            scholar_query += f' "{author_name}"'
        
        try:
            scholar_url = f"https://scholar.google.com/scholar?q={quote(scholar_query)}"
            response = self.session.get(scholar_url)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                for result in soup.find_all('div', class_='gs_r gs_or gs_scl'):
                    title_elem = result.find('h3', class_='gs_rt')
                    if title_elem:
                        link = title_elem.find('a')
                        if link and link.get('href'):
                            urls.append({
                                'url': link['href'],
                                'title': title_elem.get_text(),
                                'source': 'Google Scholar'
                            })
        except Exception as e:
            print(f"❌ Errore ricerca Google Scholar: {e}")
        
        try:
            rg_query = f'"{study_name}"'
            rg_url = f"https://www.researchgate.net/search/publication?q={quote(rg_query)}"
            response = self.session.get(rg_url)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                for result in soup.find_all('div', class_='nova-legacy-v-publication-item'):
                    title_elem = result.find('a', class_='nova-legacy-v-publication-item__title')
                    if title_elem:
                        urls.append({
                            'url': f"https://www.researchgate.net{title_elem['href']}",
                            'title': title_elem.get_text(),
                            'source': 'ResearchGate'
                        })
        except Exception as e:
            print(f"❌ Errore ricerca ResearchGate: {e}")
        
        return urls[:5]  # Massimo 5 risultati
    
    def scrape_study_content(self, url):
        """Scrapa il contenuto di uno studio scientifico"""
        try:
            print(f"🔬 Scraping studio: {url}")
            
            response = self.session.get(url, timeout=30)
            if response.status_code != 200:
                return None
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            study_info = {
                'url': url,
                'title': self._extract_title(soup),
                'authors': self._extract_authors(soup),
                'abstract': self._extract_abstract(soup),
                'methodology': self._extract_methodology(soup),
                'results': self._extract_results(soup),
                'conclusions': self._extract_conclusions(soup),
                'publication_date': self._extract_date(soup),
                'journal': self._extract_journal(soup),
                'doi': self._extract_doi(soup),
                'peer_reviewed': self._is_peer_reviewed(soup),
                'full_text': self._extract_full_text(soup)
            }
            
            return study_info
            
        except Exception as e:
            print(f"❌ Errore scraping studio {url}: {e}")
            return None
    
    def _extract_title(self, soup):
        """Estrae il titolo dello studio"""
        selectors = [
            'h1.title',
            '.publication-title',
            '.article-title',
            'h1',
            '.title',
            '[data-testid="title"]'
        ]
        
        for selector in selectors:
            elem = soup.select_one(selector)
            if elem:
                return elem.get_text().strip()
        return "Titolo non trovato"
    
    def _extract_authors(self, soup):
        """Estrae gli autori"""
        selectors = [
            '.authors',
            '.author-list',
            '.contrib-author',
            '[data-testid="authors"]',
            '.author'
        ]
        
        authors = []
        for selector in selectors:
            elems = soup.select(selector)
            for elem in elems:
                authors.append(elem.get_text().strip())
        
        return authors if authors else ["Autori non trovati"]
    
    def _extract_abstract(self, soup):
        """Estrae l'abstract"""
        selectors = [
            '.abstract',
            '.summary',
            '[data-testid="abstract"]',
            '.article-abstract',
            '.abstract-text'
        ]
        
        for selector in selectors:
            elem = soup.select_one(selector)
            if elem:
                return elem.get_text().strip()
        return "Abstract non trovato"
    
    def _extract_methodology(self, soup):
        """Estrae la metodologia"""
        methodology_keywords = ['method', 'methodology', 'methods', 'materials', 'procedures']
        
        for keyword in methodology_keywords:
            headings = soup.find_all(['h1', 'h2', 'h3', 'h4'], string=re.compile(keyword, re.I))
            for heading in headings:
                content = []
                for sibling in heading.find_next_siblings():
                    if sibling.name in ['h1', 'h2', 'h3', 'h4']:
                        break
                    if sibling.get_text().strip():
                        content.append(sibling.get_text().strip())
                
                if content:
                    return ' '.join(content[:500])  # Primi 500 caratteri
        
        return "Metodologia non trovata"
    
    def _extract_results(self, soup):
        """Estrae i risultati"""
        results_keywords = ['results', 'findings', 'outcomes', 'data']
        
        for keyword in results_keywords:
            headings = soup.find_all(['h1', 'h2', 'h3', 'h4'], string=re.compile(keyword, re.I))
            for heading in headings:
                content = []
                for sibling in heading.find_next_siblings():
                    if sibling.name in ['h1', 'h2', 'h3', 'h4']:
                        break
                    if sibling.get_text().strip():
                        content.append(sibling.get_text().strip())
                
                if content:
                    return ' '.join(content[:500])
        
        return "Risultati non trovati"
    
    def _extract_conclusions(self, soup):
        """Estrae le conclusioni"""
        conclusion_keywords = ['conclusion', 'discussion', 'summary', 'implications']
        
        for keyword in conclusion_keywords:
            headings = soup.find_all(['h1', 'h2', 'h3', 'h4'], string=re.compile(keyword, re.I))
            for heading in headings:
                content = []
                for sibling in heading.find_next_siblings():
                    if sibling.name in ['h1', 'h2', 'h3', 'h4']:
                        break
                    if sibling.get_text().strip():
                        content.append(sibling.get_text().strip())
                
                if content:
                    return ' '.join(content[:500])
        
        return "Conclusioni non trovate"
    
    def _extract_date(self, soup):
        """Estrae la data di pubblicazione"""
        date_selectors = [
            '.publication-date',
            '.date',
            '.published-date',
            '[data-testid="date"]',
            'time'
        ]
        
        for selector in date_selectors:
            elem = soup.select_one(selector)
            if elem:
                return elem.get_text().strip()
        
        return "Data non trovata"
    
    def _extract_journal(self, soup):
        """Estrae il nome della rivista"""
        journal_selectors = [
            '.journal-name',
            '.publication-title',
            '.journal',
            '[data-testid="journal"]'
        ]
        
        for selector in journal_selectors:
            elem = soup.select_one(selector)
            if elem:
                return elem.get_text().strip()
        
        return "Rivista non trovata"
    
    def _extract_doi(self, soup):
        """Estrae il DOI"""
        doi_pattern = r'10\.\d{4,}/[-._;()/:\w]+'
        
        text = soup.get_text()
        doi_match = re.search(doi_pattern, text)
        if doi_match:
            return doi_match.group()
        
        doi_selectors = ['.doi', '[data-testid="doi"]', '.identifier']
        for selector in doi_selectors:
            elem = soup.select_one(selector)
            if elem:
                doi_match = re.search(doi_pattern, elem.get_text())
                if doi_match:
                    return doi_match.group()
        
        return "DOI non trovato"
    
    def _is_peer_reviewed(self, soup):
        """Determina se è peer-reviewed"""
        peer_reviewed_indicators = [
            'peer-reviewed',
            'peer review',
            'refereed',
            'academic journal',
            'scientific journal'
        ]
        
        text = soup.get_text().lower()
        for indicator in peer_reviewed_indicators:
            if indicator in text:
                return True
        
        return False
    
    def _extract_full_text(self, soup):
        """Estrae il testo completo dello studio"""
        for elem in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
            elem.decompose()
        
        paragraphs = soup.find_all('p')
        text_parts = []
        
        for p in paragraphs:
            text = p.get_text().strip()
            if len(text) > 50:  # Solo paragrafi significativi
                text_parts.append(text)
        
        return ' '.join(text_parts[:2000])  # Primi 2000 caratteri
    
    def analyze_study_quality(self, study_info):
        """Analizza la qualità dello studio"""
        quality_score = 0
        issues = []
        strengths = []
        
        if study_info.get('abstract'):
            quality_score += 2
            strengths.append("Abstract presente")
        else:
            issues.append("Manca l'abstract")
        
        if study_info.get('methodology'):
            quality_score += 3
            strengths.append("Metodologia descritta")
        else:
            issues.append("Manca la descrizione metodologica")
        
        if study_info.get('results'):
            quality_score += 2
            strengths.append("Risultati presentati")
        else:
            issues.append("Mancano i risultati")
        
        if study_info.get('conclusions'):
            quality_score += 1
            strengths.append("Conclusioni presenti")
        else:
            issues.append("Mancano le conclusioni")
        
        if study_info.get('doi'):
            quality_score += 1
            strengths.append("DOI presente")
        else:
            issues.append("Manca il DOI")
        
        if study_info.get('peer_reviewed'):
            quality_score += 2
            strengths.append("Peer-reviewed")
        else:
            issues.append("Non è peer-reviewed")
        
        journal = study_info.get('journal', '').lower()
        if any(publisher in journal for publisher in ['wiley', 'springer', 'elsevier', 'nature', 'science']):
            quality_score += 1
            strengths.append("Rivista prestigiosa")
        else:
            issues.append("Rivista di dubbia qualità")
        
        return {
            'score': quality_score,
            'max_score': 12,
            'percentage': (quality_score / 12) * 100,
            'issues': issues,
            'strengths': strengths,
            'overall_quality': 'Alta' if quality_score >= 8 else 'Media' if quality_score >= 5 else 'Bassa'
        } 