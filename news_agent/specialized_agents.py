
import json
import re
from .ai_providers import create_ai_provider
from .serpapi_integration import SerpAPIIntegration
from .settings import load_settings

class SpecializedAgent:
    def __init__(self, specialization, ai_provider):
        self.specialization = specialization
        self.ai_provider = ai_provider
    
    def generate_search_queries(self, article, analysis, language='it'):
        raise NotImplementedError
    
    def evaluate_results(self, queries, results, language='it', article=None):
        raise NotImplementedError

class PoliticalAgent(SpecializedAgent):
    def __init__(self, ai_provider):
        super().__init__("politico", ai_provider)
    
    def generate_search_queries(self, article, analysis, language='it'):
        
        prompt = f"""
        Sei un esperto di politica. Genera query per verificare questa notizia politica.
        
        NOTIZIA:
        Titolo: {article.get('title', 'N/A')}
        Contenuto: {article.get('content', article.get('summary', 'N/A'))}
        
        ANALISI CRITICA:
        {analysis}
        
        Genera 3-5 query di ricerca in {language} per verificare questa notizia politica.
        Le query devono cercare:
        1. Dichiarazioni ufficiali di politici/governo
        2. Comunicati stampa ufficiali
        3. Conferme da fonti politiche affidabili
        4. Reazioni di altri partiti/politici
        
        Restituisci solo un array JSON di stringhe:
        ["query 1", "query 2", "query 3"]
        """
        
        try:
            response = self.ai_provider.generate(prompt, max_tokens=300)
            queries = json.loads(response)
            return queries if isinstance(queries, list) else []
        except:
            return [
                f"dichiarazione ufficiale {article.get('title', '')}",
                f"comunicato stampa {article.get('title', '')}",
                f"reazione politica {article.get('title', '')}"
            ]
    
    def evaluate_results(self, queries, results, language='it', agent_info=None, article=None):
        
        political_context = ""
        if agent_info:
            politici = agent_info.get('politici_coinvolti', [])
            istituzioni = agent_info.get('istituzioni', [])
            if politici or istituzioni:
                political_context = f"""
INFORMAZIONI SPECIFICHE IDENTIFICATE:
- Politici coinvolti: {', '.join(politici) if politici else 'Nessuno identificato'}
- Istituzioni coinvolte: {', '.join(istituzioni) if istituzioni else 'Nessuna identificata'}
- Entità principali: {', '.join(agent_info.get('entita_principali', []))}
- Eventi chiave: {', '.join(agent_info.get('eventi_chiave', []))}
"""
        
        prompt = f"""
        Sei un esperto di politica. Valuta questi risultati per una notizia politica.
        
        QUERY ESEGUITE:
        {queries}
        
        RISULTATI TROVATI:
        {results}
        
        {political_context}
        
        Valuta in {language} se i risultati confermano o smentiscono la notizia.
        Considera:
        - Presenza di dichiarazioni ufficiali
        - Comunicati stampa ufficiali
        - Conferme da fonti politiche affidabili
        - Reazioni di altri partiti/politici
        - Verifica specifica dei politici e istituzioni identificati
        
        Restituisci un JSON:
        {{
            "conferma": true/false,
            "evidenze_a_favore": ["evidenza 1", "evidenza 2"],
            "evidenze_contro": ["evidenza 1", "evidenza 2"],
            "livello_affidabilita": 1-10,
            "spiegazione": "spiegazione dettagliata"
        }}
        """
        
        try:
            response = self.ai_provider.generate(prompt, max_tokens=400)
            return json.loads(response)
        except Exception as e:
            return {
                "conferma": False,
                "evidenze_a_favore": [],
                "evidenze_contro": ["Impossibile valutare risultati"],
                "livello_affidabilita": 5,
                "spiegazione": f"Impossibile valutare i risultati delle ricerche. La notizia potrebbe essere vera ma non verificabile con le fonti attuali."
            }

class TechnologyAgent(SpecializedAgent):
    def __init__(self, ai_provider):
        super().__init__("tecnologico", ai_provider)
    
    def generate_search_queries(self, article, analysis, language='it'):
        
        prompt = f"""
        Sei un esperto di tecnologia e intelligenza artificiale. Genera query per verificare questa notizia tech.
        
        NOTIZIA:
        Titolo: {article.get('title', 'N/A')}
        Contenuto: {article.get('content', article.get('summary', 'N/A'))}
        
        ANALISI CRITICA:
        {analysis}
        
        Genera 3-5 query di ricerca in {language} per verificare questa notizia tecnologica.
        Le query devono cercare:
        1. Comunicati ufficiali dell'azienda
        2. Annunci ufficiali su blog/siti aziendali
        3. Documenti SEC o finanziari
        4. Conferme da fonti tech affidabili
        
        Restituisci solo un array JSON di stringhe:
        ["query 1", "query 2", "query 3"]
        """
        
        try:
            response = self.ai_provider.generate(prompt, max_tokens=300)
            queries = json.loads(response)
            return queries if isinstance(queries, list) else []
        except:
            return [
                f"annuncio ufficiale {article.get('title', '')}",
                f"comunicato stampa {article.get('title', '')}",
                f"blog ufficiale {article.get('title', '')}"
            ]
    
    def evaluate_results(self, queries, results, language='it', agent_info=None, article=None):
        tech_context = ""
        if agent_info:
            aziende = agent_info.get('aziende_tech', [])
            tecnologie = agent_info.get('tecnologie', [])
            if aziende or tecnologie:
                tech_context = f"""
INFORMAZIONI SPECIFICHE IDENTIFICATE:
- Aziende tech coinvolte: {', '.join(aziende) if aziende else 'Nessuna identificata'}
- Tecnologie menzionate: {', '.join(tecnologie) if tecnologie else 'Nessuna identificata'}
- Entità principali: {', '.join(agent_info.get('entita_principali', []))}
- Eventi chiave: {', '.join(agent_info.get('eventi_chiave', []))}
"""
        
        prompt = f"""
        Sei un esperto di tecnologia. Valuta questi risultati per una notizia tech.
        
        QUERY ESEGUITE:
        {queries}
        
        RISULTATI TROVATI:
        {results}
        
        {tech_context}
        
        Valuta in {language} se i risultati confermano o smentiscono la notizia.
        Considera:
        - Presenza di comunicati ufficiali aziendali
        - Annunci su blog/siti ufficiali
        - Documenti SEC o finanziari
        - Conferme da fonti tech affidabili
        - Verifica specifica delle aziende e tecnologie identificate
        - Se c'è del codice, verifica anche quello
        - Guarda se la notizia è veramente tecnica oppure palese marketing
        
        Restituisci un JSON:
        {{
            "conferma": true/false,
            "evidenze_a_favore": ["evidenza 1", "evidenza 2"],
            "evidenze_contro": ["evidenza 1", "evidenza 2"],
            "livello_affidabilita": 1-10,
            "spiegazione": "spiegazione dettagliata"
        }}
        """
        
        try:
            response = self.ai_provider.generate(prompt, max_tokens=400)
            return json.loads(response)
        except Exception as e:
            return {
                "conferma": False,
                "evidenze_a_favore": [],
                "evidenze_contro": ["Impossibile valutare risultati"],
                "livello_affidabilita": 5,
                "spiegazione": f"Impossibile valutare i risultati delle ricerche. La notizia potrebbe essere vera ma non verificabile con le fonti attuali."
            }

class ScientificAgent(SpecializedAgent):
    def __init__(self, ai_provider):
        super().__init__("scientifico", ai_provider)
    
    def generate_search_queries(self, article, analysis, language='it'):
        """Genera query per verificare notizie scientifiche e trovare gli studi citati"""
        
        prompt = f"""
        Sei un esperto di ricerca scientifica. Genera query per verificare questa notizia scientifica.
        
        NOTIZIA:
        Titolo: {article.get('title', 'N/A')}
        Contenuto: {article.get('content', article.get('summary', 'N/A'))}
        
        ANALISI CRITICA:
        {analysis}
        
        Genera 3-5 query di ricerca in {language} per verificare questa notizia scientifica.
        
        OBIETTIVI:
        1. TROVARE LO STUDIO CITATO: Cerca il paper/studio specifico menzionato
        2. VERIFICARE LA PUBBLICAZIONE: Controlla se è stato pubblicato su riviste peer-reviewed
        3. ANALIZZARE LE LACUNE: Cerca critiche, errori, o limitazioni dello studio
        4. CONFERME DA FONTI SCIENTIFICHE: Università, istituti di ricerca, database scientifici
        
        TIPI DI QUERY:
        - Nome specifico dello studio/ricercatore + "paper" o "pubblicazione"
        - Nome rivista scientifica + argomento
        - "critiche" + nome studio/ricercatore
        - "errori" + nome studio/ricercatore
        - "limiti" + nome studio/ricercatore
        - Conferme da fonti ufficiali
        
        Restituisci solo un array JSON di stringhe:
        ["query 1", "query 2", "query 3"]
        """
        
        try:
            response = self.ai_provider.generate(prompt, max_tokens=300)
            queries = json.loads(response)
            return queries if isinstance(queries, list) else []
        except:
            return [
                f"studio scientifico {article.get('title', '')}",
                f"paper ricerca {article.get('title', '')}",
                f"pubblicazione {article.get('title', '')}"
            ]
    
    def evaluate_results(self, queries, results, language='it', study_info=None, article=None):
        """Valuta i risultati per notizie scientifiche e analizza le lacune degli studi"""
        
        if study_info:
            study_analysis = self._analyze_specific_study_with_info(queries, results, study_info)
        else:
            study_analysis = self._analyze_specific_study(queries, results)
        
        prompt = f"""
        Sei un CRITICO METODOLOGICO SCIENTIFICO RIGOROSO. Il tuo compito è VALUTARE LA QUALITÀ SCIENTIFICA DELLO STUDIO con criteri FERREI.
        
        NOTIZIA DA ANALIZZARE:
        {article.get('title', 'N/A')}
        {article.get('content', article.get('summary', 'N/A'))}

        RISULTATI DELLA RICERCA:
        {results}

        ANALISI DELLO STUDIO:
        {study_analysis}

        IL TUO COMPITO: Valuta la QUALITÀ METODOLOGICA dello studio scientifico menzionato nella notizia.
        
        CRITERI DI VALUTAZIONE METODOLOGICA

        1. Metodo di ricerca: Il protocollo sperimentale è rigoroso e scientificamente valido?
        2. Accesso ai dati: C’è accesso diretto ai dati grezzi, ai campioni originali o agli oggetti d’analisi?
        3. Strumentazione: Sono stati usati strumenti e tecniche adeguati, affidabili e documentati?
        4. Controlli e replicabilità: Sono presenti controlli sperimentali solidi e la piena replicabilità?
        5. Limitazioni metodologiche: Ci sono ricostruzioni, simulazioni, software non validati o strumenti amatoriali?
        6. Uso di modelli: L’eventuale utilizzo di modelli matematici/computazionali viene esplicitato come semplice proiezione e non come prova oggettiva?

        LIMITAZIONI CRITICHE (SEGNALA SEMPRE):
        - Ricostruzioni 3D senza accesso diretto = LIMITAZIONE GRAVE
        - Software gratuito/amatoriale per analisi complesse = LIMITAZIONE
        - Mancanza di peer-review = LIMITAZIONE
        - Studi su repliche/simulazioni = LIMITAZIONE
        - Mancanza di controlli sperimentali = LIMITAZIONE
        - Modelli computazionali usati come "prova" = LIMITAZIONE

        REGOLE FERREE (SEGUI SEMPRE):
        - I MODELLI/SIMULAZIONI/RICOSTRUZIONI NON SONO PROVE SPERIMENTALI
        - RICOSTRUZIONI 3D = NON PROVE OGGETTIVE
        - SOFTWARE AMATORIALE = LIMITAZIONE METODOLOGICA GRAVE
        - SENZA ACCESSO DIRETTO AI DATI = AFFIDABILITÀ BASSA
        - MANCANZA DI PEER-REVIEW = LIMITAZIONE GRAVE
        - MANCANZA DI CONTROLLI SPERIMENTALI = LIMITAZIONE GRAVE
        - Utilizzo di modelli matematici, IA o simulazioni come “prova” invece che come mera proiezione → Limite metodologico da evidenziare (i modelli NON costituiscono prova sperimentale)

        VALUTAZIONE RIGOROSA:
        - Se ci sono LIMITAZIONI GRAVI = AFFIDABILITÀ BASSA (1-4/10)
        - Se ci sono LIMITAZIONI = AFFIDABILITÀ MODERATA (5-7/10)
        - Solo se METODOLOGIA PERFETTA = AFFIDABILITÀ ALTA (8-10/10)

        ANALISI E DECISIONE

        - Se il metodo presenta limiti gravi o non consente verifica indipendente, l’affidabilità va drasticamente ridotta.
        - Metodi indiretti, ricostruzioni, simulazioni o modelli devono essere segnalati come limiti.
        - Senza accesso diretto ai dati/campioni originali, la solidità della ricerca è fortemente compromessa.
        - Se il metodo non giustifica le conclusioni, la notizia va considerata probabilmente falsa.
        - Ignora il prestigio, la fonte o i pareri istituzionali: conta solo la trasparenza metodologica e la verificabilità dei fatti.

        VALUTA SOLO:
        - Rigore metodologico
        - Accesso ai dati originali
        - Validazione strumentale
        - Controlli sperimentali
        - Replicabilità

        IGNORA COMPLETAMENTE:
        - Prestigio delle fonti
        - Autorevolezza istituzionale
        - Fama dei ricercatori
        - Risultati dello studio (valuta solo il metodo)

        Restituisci un JSON:
        {{
            "conferma": true/false,
            "evidenze_a_favore": ["evidenza tecnica 1", "evidenza tecnica 2"],
            "evidenze_contro": ["limitazione metodologica 1", "limitazione metodologica 2"],
            "livello_affidabilita": 1-10,
            "spiegazione": "VALUTAZIONE METODOLOGICA RIGOROSA: qualità scientifica, limitazioni, validità sperimentale"
        }}
        """
        
        try:
                response = self.ai_provider.generate(prompt, max_tokens=400)
                
                cleaned_response = self._extract_json_from_response(response)
                
                try:
                    evaluation = json.loads(cleaned_response)
                    return evaluation
                except json.JSONDecodeError:
                    fallback_evaluation = self._create_fallback_evaluation(response, results)
                    return fallback_evaluation
                
        except Exception as e:
            return {
                "conferma": False,
                "evidenze_a_favore": [],
                "evidenze_contro": ["Impossibile valutare risultati"],
                "livello_affidabilita": 5,
                "spiegazione": f"Impossibile valutare i risultati delle ricerche. La notizia potrebbe essere vera ma non verificabile con le fonti attuali."
            }
    
    def _analyze_specific_study(self, queries, results):
        """Analizza lo studio specifico menzionato nella notizia"""
        try:
            from .scientific_study_scraper import ScientificStudyScraper
            
            scraper = ScientificStudyScraper()
            
            study_info = self._extract_study_info(queries, results)
            
            if not study_info:
                return "Nessuna informazione sullo studio trovata"
            
            study_urls = scraper.find_study_urls(
                study_info.get('study_name', ''),
                study_info.get('author_name', '')
            )
            
            if not study_urls:
                return "Nessun URL dello studio trovato"
            
            study_url = study_urls[0]['url']
            study_content = scraper.scrape_study_content(study_url)
            
            if not study_content:
                return "Impossibile accedere al contenuto dello studio"
            
            quality_analysis = scraper.analyze_study_quality(study_content)
            analysis = f"""
ANALISI DELLO STUDIO SPECIFICO:
Titolo: {study_content.get('title', 'N/A')}
Autori: {', '.join(study_content.get('authors', []))}
Rivista: {study_content.get('journal', 'N/A')}
DOI: {study_content.get('doi', 'N/A')}
Data: {study_content.get('publication_date', 'N/A')}
Peer-reviewed: {'Sì' if study_content.get('peer_reviewed') else 'No'}

QUALITÀ DELLO STUDIO:
Punteggio: {quality_analysis['score']}/{quality_analysis['max_score']} ({quality_analysis['percentage']:.1f}%)
Qualità generale: {quality_analysis['overall_quality']}

PUNTI DI FORZA:
{chr(10).join(f'- {strength}' for strength in quality_analysis['strengths'])}

PROBLEMI IDENTIFICATI:
{chr(10).join(f'- {issue}' for issue in quality_analysis['issues'])}

ABSTRACT:
{study_content.get('abstract', 'N/A')[:300]}...

METODOLOGIA:
{study_content.get('methodology', 'N/A')[:300]}...

RISULTATI:
{study_content.get('results', 'N/A')[:300]}...

CONCLUSIONI:
{study_content.get('conclusions', 'N/A')[:300]}...
"""
            
            return analysis
            
        except Exception as e:
            return f"Errore nell'analisi dello studio: {e}"
    
    def _analyze_specific_study_with_info(self, queries, results, study_info):
        """Analizza lo studio specifico usando le informazioni fornite dall'orchestratore"""
        try:
            from .scientific_study_scraper import ScientificStudyScraper
            
            scraper = ScientificStudyScraper()
            
            study_name = study_info.get('study_name', '')
            author_name = study_info.get('author_name', '')
            journal = study_info.get('journal', '')
            
            if not study_name and not author_name:
                return "Informazioni insufficienti sullo studio"
            
            search_terms = []
            if author_name and study_name:
                search_terms.append(f"{author_name} {study_name}")
                search_terms.append(f"{study_name} {author_name}")
            if author_name:
                search_terms.append(f"{author_name} studio")
                search_terms.append(f"{author_name} ricerca")
                search_terms.append(f"{author_name} paper")
            if study_name:
                search_terms.append(f"{study_name} studio")
                search_terms.append(f"{study_name} ricerca")
            if journal and author_name:
                search_terms.append(f"{journal} {author_name}")
                search_terms.append(f"{author_name} {journal}")
            
            study_urls = []
            for term in search_terms:
                urls = scraper.find_study_urls(term, author_name)
                if urls:
                    study_urls.extend(urls)
                    break
            
            if not study_urls:
                return f"Nessun URL trovato per {author_name or 'autore sconosciuto'} - {study_name or 'studio sconosciuto'}"
            
            study_url = study_urls[0]['url']
            study_content = scraper.scrape_study_content(study_url)
            
            if not study_content:
                return f"Impossibile accedere al contenuto dello studio di {author_name or 'autore sconosciuto'}"
            
            quality_analysis = scraper.analyze_study_quality(study_content)
            
            analysis = f"""
ANALISI DELLO STUDIO SPECIFICO:
Titolo: {study_content.get('title', 'N/A')}
Autori: {', '.join(study_content.get('authors', []))}
Rivista: {study_content.get('journal', journal or 'N/A')}
DOI: {study_content.get('doi', 'N/A')}
Data: {study_content.get('publication_date', 'N/A')}
Peer-reviewed: {'Sì' if study_content.get('peer_reviewed') else 'No'}

QUALITÀ DELLO STUDIO:
Punteggio: {quality_analysis['score']}/{quality_analysis['max_score']} ({quality_analysis['percentage']:.1f}%)
Qualità generale: {quality_analysis['overall_quality']}

PUNTI DI FORZA:
{chr(10).join(f'- {strength}' for strength in quality_analysis['strengths'])}

PROBLEMI IDENTIFICATI:
{chr(10).join(f'- {issue}' for issue in quality_analysis['issues'])}

ABSTRACT:
{study_content.get('abstract', 'N/A')[:300]}...

METODOLOGIA:
{study_content.get('methodology', 'N/A')[:300]}...

RISULTATI:
{study_content.get('results', 'N/A')[:300]}...

CONCLUSIONI:
{study_content.get('conclusions', 'N/A')[:300]}...

ANALISI CRITICA SPECIFICA:
- Autore identificato: {author_name or 'Non identificato'}
- Studio identificato: {study_name or 'Non identificato'}
- Rivista identificata: {journal or 'Non identificata'}
- Ricerca specifica eseguita: {'Sì' if study_urls else 'No'}
- Termini di ricerca utilizzati: {', '.join(search_terms[:3])}
"""
            
            return analysis
            
        except Exception as e:
            return f"Errore nell'analisi dello studio specifico: {e}"
    
    def _extract_study_info(self, queries, results):
        """Estrae informazioni sullo studio dalle query e risultati"""
        study_name = None
        author_name = None
        
        author_patterns = [
            r'(\w+\s+\w+)\s+studio',  # "Cicero Moraes studio"
            r'studio\s+(\w+\s+\w+)',  # "studio Cicero Moraes"
            r'(\w+\s+\w+)\s+pubblicazione',  # "Cicero Moraes pubblicazione"
            r'(\w+\s+\w+)\s+paper',  # "Cicero Moraes paper"
            r'(\w+\s+\w+)\s+ricerca',  # "Cicero Moraes ricerca"
            r'ricerca\s+(\w+\s+\w+)',  # "ricerca Cicero Moraes"
        ]
        
        for query in queries:
            if 'cicero' in query.lower() and 'moraes' in query.lower():
                author_name = "Cicero Moraes"
                break
            
            for pattern in author_patterns:
                match = re.search(pattern, query, re.IGNORECASE)
                if match:
                    potential_name = match.group(1).strip()
                    if len(potential_name.split()) >= 2:
                        author_name = potential_name
                        break
            if author_name:
                break
        
        if not author_name:
            if 'cicero' in results.lower() and 'moraes' in results.lower():
                author_name = "Cicero Moraes"
            else:
                for pattern in author_patterns:
                    match = re.search(pattern, results, re.IGNORECASE)
                    if match:
                        potential_name = match.group(1).strip()
                        if len(potential_name.split()) >= 2:
                            author_name = potential_name
                            break
        
        study_keywords = ['sindone', 'torino', 'shroud']
        for query in queries:
            if any(keyword in query.lower() for keyword in study_keywords):
                study_name = "Sindone di Torino"
                break
        
        if not study_name:
            if any(keyword in results.lower() for keyword in study_keywords):
                study_name = "Sindone di Torino"
        
        return {
            'study_name': study_name,
            'author_name': author_name
        }
    
    def _extract_json_from_response(self, response):
        """Estrae JSON da una risposta che può contenere testo extra"""
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response, re.DOTALL)
        if json_match:
            return json_match.group(1)
        
        json_match = re.search(r'(\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\})', response, re.DOTALL)
        if json_match:
            return json_match.group(1)
        
        json_match = re.search(r'(\{[^}]*"conferma"[^}]*\})', response, re.DOTALL)
        if json_match:
            return json_match.group(1)
        
        return response.strip()
    
    def _create_fallback_evaluation(self, response, results):
        """Crea una valutazione di fallback analizzando il testo della risposta"""
        response_lower = response.lower()

        conferma = False
        if any(word in response_lower for word in ['conferma', 'vero', 'verificato', 'affermato']):
            conferma = True
        elif any(word in response_lower for word in ['falso', 'smentito', 'errato', 'non verificato']):
            conferma = False
        
        evidenze_a_favore = []
        evidenze_contro = []
        
        if 'numerosi articoli' in response_lower or 'fonti confermano' in response_lower:
            evidenze_a_favore.append("Presenza di fonti che confermano la notizia")
        
        if 'critiche' in response_lower or 'errori' in response_lower or 'problemi' in response_lower:
            evidenze_contro.append("Presenza di critiche o errori identificati")
        
        if 'peer-reviewed' in response_lower and 'non' in response_lower:
            evidenze_contro.append("Lo studio non è peer-reviewed")
        
        if 'doi' in response_lower and 'non' in response_lower:
            evidenze_contro.append("Manca il DOI")
        

        livello_affidabilita = 5 
        
        if conferma and len(evidenze_a_favore) > len(evidenze_contro):
            livello_affidabilita = 7
        elif not conferma or len(evidenze_contro) > len(evidenze_a_favore):
            livello_affidabilita = 3
        

        spiegazione = "Valutazione basata su analisi del testo della risposta AI. "
        if conferma:
            spiegazione += "La notizia sembra essere confermata dalle fonti disponibili."
        else:
            spiegazione += "La notizia presenta criticità o mancanza di conferme affidabili."
        
        return {
            "conferma": conferma,
            "evidenze_a_favore": evidenze_a_favore if evidenze_a_favore else ["Analisi basata su fonti disponibili"],
            "evidenze_contro": evidenze_contro if evidenze_contro else ["Valutazione limitata dalla qualità delle fonti"],
            "livello_affidabilita": livello_affidabilita,
            "spiegazione": spiegazione
        }

class EconomicAgent(SpecializedAgent):
    def __init__(self, ai_provider):
        super().__init__("economico", ai_provider)
    
    def generate_search_queries(self, article, analysis, language='it'):
        """Genera query per verificare notizie economiche"""
        
        prompt = f"""
        Sei un esperto di economia e finanza. Genera query per verificare questa notizia economica.
        
        NOTIZIA:
        Titolo: {article.get('title', 'N/A')}
        Contenuto: {article.get('content', article.get('summary', 'N/A'))}
        
        ANALISI CRITICA:
        {analysis}
        
        Genera 3-5 query di ricerca in {language} per verificare questa notizia economica.
        Le query devono cercare:
        1. Report finanziari ufficiali
        2. Dati economici da fonti ufficiali
        3. Analisi di esperti economici
        4. Conferme da agenzie di rating
        
        Restituisci solo un array JSON di stringhe:
        ["query 1", "query 2", "query 3"]
        """
        
        try:
            response = self.ai_provider.generate(prompt, max_tokens=300)
            queries = json.loads(response)
            return queries if isinstance(queries, list) else []
        except:
            return [
                f"report finanziario {article.get('title', '')}",
                f"dati economici {article.get('title', '')}",
                f"analisi economica {article.get('title', '')}"
            ]
    
    def evaluate_results(self, queries, results, language='it', agent_info=None, article=None):
        """Valuta i risultati per notizie economiche"""
        
        economic_context = ""
        if agent_info:
            entita = agent_info.get('entita_principali', [])
            eventi = agent_info.get('eventi_chiave', [])
            fonti = agent_info.get('fonti_citate', [])
            dettagli = agent_info.get('dettagli_rilevanti', [])
            if entita or eventi or fonti or dettagli:
                economic_context = f"""
INFORMAZIONI SPECIFICHE IDENTIFICATE:
- Entità economiche: {', '.join(entita) if entita else 'Nessuna identificata'}
- Eventi economici: {', '.join(eventi) if eventi else 'Nessuno identificato'}
- Fonti economiche: {', '.join(fonti) if fonti else 'Nessuna identificata'}
- Dettagli economici: {', '.join(dettagli) if dettagli else 'Nessuno identificato'}
"""
        
        prompt = f"""
        Sei un esperto di economia. Valuta questi risultati per una notizia economica.
        
        QUERY ESEGUITE:
        {queries}
        
        RISULTATI TROVATI:
        {results}
        
        {economic_context}
        
        Valuta in {language} se i risultati confermano o smentiscono la notizia.
        Considera:
        - Presenza di report finanziari ufficiali
        - Dati economici da fonti ufficiali
        - Analisi di esperti economici
        - Conferme da agenzie di rating
        
        Restituisci un JSON:
        {{
            "conferma": true/false,
            "evidenze_a_favore": ["evidenza 1", "evidenza 2"],
            "evidenze_contro": ["evidenza 1", "evidenza 2"],
            "livello_affidabilita": 1-10,
            "spiegazione": "spiegazione dettagliata"
        }}
        """
        
        try:
            response = self.ai_provider.generate(prompt, max_tokens=400)
            return json.loads(response)
        except Exception as e:
            return {
                "conferma": False,
                "evidenze_a_favore": [],
                "evidenze_contro": ["Impossibile valutare risultati"],
                "livello_affidabilita": 5,
                "spiegazione": f"Impossibile valutare i risultati delle ricerche. La notizia potrebbe essere vera ma non verificabile con le fonti attuali."
            }

class UniversalAgent(SpecializedAgent):
    def __init__(self, ai_provider):
        super().__init__("universale", ai_provider)
    
    def generate_search_queries(self, article, analysis, language='it'):
        """Genera query universali per verificare qualsiasi notizia"""
        
        prompt = f"""
        Sei un esperto di fact-checking e verifica notizie. Genera query SEMPLICI per verificare questa notizia.
        
        NOTIZIA:
        Titolo: {article.get('title', 'N/A')}
        Contenuto: {article.get('content', article.get('summary', 'N/A'))}
        
        ANALISI CRITICA:
        {analysis}
        
        Genera 3 query di ricerca SEMPLICI in {language} per verificare questa notizia.
        
        REGOLE IMPORTANTI:
        - Le query devono essere BREVI (massimo 4-5 parole)
        - Usa solo le parole chiave più importanti dal titolo
        - Evita query troppo specifiche o lunghe
        - Cerca notizie generali, non dettagli specifici
        
        ESEMPI DI QUERY SEMPLICI:
        - "Trump dazi chip" (invece di "Dichiarazioni ufficiali Trump dazi 100% chip esteri")
        - "Gaza IDF" (invece di "Dichiarazioni ufficiali IDF occupazione Striscia di Gaza")
        - "Netanyahu Gaza" (invece di "Comunicati stampa Netanyahu operazione militare Gaza")
        
        Restituisci solo un array JSON di stringhe:
        ["query 1", "query 2", "query 3"]
        """
        
        try:
            response = self.ai_provider.generate(prompt, max_tokens=400)
            queries = json.loads(response)
            return queries if isinstance(queries, list) else []
        except:

            title = article.get('title', '')

            words = title.split()[:4]
            keywords = ' '.join(words)
            return [
                f"{keywords}",
                f"notizia {keywords}",
                f"ultime notizie {keywords}"
            ]
    
    def evaluate_results(self, queries, results, language='it', agent_info=None, article=None):
        """Valuta i risultati in modo universale per qualsiasi notizia"""
        
        universal_context = ""
        if agent_info:
            entita = agent_info.get('entita_principali', [])
            eventi = agent_info.get('eventi_chiave', [])
            fonti = agent_info.get('fonti_citate', [])
            dettagli = agent_info.get('dettagli_rilevanti', [])
            if entita or eventi or fonti or dettagli:
                universal_context = f"""
INFORMAZIONI SPECIFICHE IDENTIFICATE:
- Entità principali: {', '.join(entita) if entita else 'Nessuna identificata'}
- Eventi chiave: {', '.join(eventi) if eventi else 'Nessuno identificato'}
- Fonti citate: {', '.join(fonti) if fonti else 'Nessuna identificata'}
- Dettagli rilevanti: {', '.join(dettagli) if dettagli else 'Nessuno identificato'}
"""
        
        prompt = f"""
        Sei un esperto di fact-checking. Valuta questi risultati per verificare la notizia.
        
        QUERY ESEGUITE:
        {queries}
        
        RISULTATI TROVATI:
        {results}
        
        {universal_context}
        
        Valuta in {language} se i risultati confermano o smentiscono la notizia.
        
        CRITERI DI VALUTAZIONE:
        1. PRESENZA DI CONFERME: Fonti ufficiali, dichiarazioni autorevoli
        2. COERENZA: I risultati supportano la notizia?
        3. CONTRADDIZIONI: Ci sono smentite o contraddizioni?
        4. AFFIDABILITÀ: Le fonti sono credibili?
        5. TEMPORALITÀ: I risultati sono recenti e pertinenti?
        6. METODOLOGIA: Se è una notizia scientifica, valuta anche il metodo
        
        ATTENZIONE PER NOTIZIE SCIENTIFICHE:
        - Se la notizia riguarda studi/ricerche, valuta anche la metodologia
        - Ricostruzioni 3D, simulazioni, software gratuiti = limitazioni
        - Mancanza di accesso diretto ai dati = limitazione
        - Studi non peer-reviewed = limitazione
        
        Restituisci un JSON:
        {{
            "conferma": true/false,
            "evidenze_a_favore": ["evidenza 1", "evidenza 2"],
            "evidenze_contro": ["evidenza 1", "evidenza 2"],
            "livello_affidabilita": 1-10,
            "spiegazione": "spiegazione dettagliata basata sui criteri"
        }}
        """
        
        try:
            response = self.ai_provider.generate(prompt, max_tokens=500)
            return json.loads(response)
        except Exception as e:
            return {
                "conferma": False,
                "evidenze_a_favore": [],
                "evidenze_contro": ["Impossibile valutare risultati"],
                "livello_affidabilita": 5,
                "spiegazione": f"Impossibile valutare i risultati delle ricerche. La notizia potrebbe essere vera ma non verificabile con le fonti attuali."
            }

class AgentManager:
    def __init__(self):
        from .settings import load_settings
        self.settings = load_settings()
        self.ai_provider = create_ai_provider(self.settings.get('provider', 'ollama'), self.settings)
        

        self.universal_agent = UniversalAgent(self.ai_provider)
        

        self.agents = {
            'politico': PoliticalAgent(self.ai_provider),
            'tecnologico': TechnologyAgent(self.ai_provider),
            'scientifico': ScientificAgent(self.ai_provider),
            'economico': EconomicAgent(self.ai_provider),
            'cronaca': self.universal_agent, 
            'universale': self.universal_agent
        }
        
        self.agent_icons = {
            'scientifico': '🔬',
            'politico': '🏛️',
            'tecnologico': '💻',
            'economico': '💰',
            'universale': '🌍',
            'cronaca': '📰'
        }
    
    def get_agent_icon(self, agent_name):
        """Restituisce l'icona per un agente specifico"""
        return self.agent_icons.get(agent_name.lower(), '🤖')

    def detect_domain(self, article, analysis):
        """Rileva il dominio della notizia in modo intelligente e generico"""
        
        prompt = f"""
        Analizza questa notizia e classificala nel dominio più appropriato.
        
        NOTIZIA:
        Titolo: {article.get('title', 'N/A')}
        Contenuto: {article.get('content', article.get('summary', 'N/A'))}
        
        ANALISI CRITICA:
        {analysis}
        
        Classifica la notizia in uno di questi domini:
        - "politico" 🏛️: politica, governo, elezioni, leggi, partiti, ministri, parlamento, CPI, denunce politiche, accuse tra partiti, politica internazionale, presidenti, capi di stato, guerra, conflitti, diplomazia, negoziati
        - "tecnologico" 💻: tecnologia, AI, startup, big tech, software, computer, innovazione digitale, app, social media
        - "scientifico" 🔬: ricerca, studi, scienza, medicina, università, laboratori, scoperte scientifiche, salute
        - "economico" 💰: economia, finanza, mercati, business, PIL, inflazione, crisi economiche, aziende, lavoro
        - "cronaca" 📰: eventi, incidenti, cronaca locale, omicidi, rapine, terremoti, meteo, clima, disastri naturali, alluvioni, siccità, ondate di calore, maltempo
        
        REGOLE GENERICHE:
        1. Analizza il CONTENUTO, non solo le parole chiave
        2. Considera il CONTESTO e l'ARGOMENTO principale
        3. Se la notizia è su un evento/accadimento → "cronaca"
        4. Se la notizia è su decisioni/azioni di governo → "politico"
        5. Se la notizia è su innovazioni/tecnologie → "tecnologico"
        6. Se la notizia è su studi/ricerche/archeologia/storia/medicina → "scientifico"
        7. Se la notizia è su mercati/finanze → "economico"
        
        REGOLE SPECIFICHE:
        - Se la notizia contiene "studio", "ricerca", "scienziati", "ricercatori" → "scientifico" 🔬
        - Sindone di Torino, archeologia, studi storici → "scientifico" 🔬
        - Ricerche mediche, scoperte scientifiche → "scientifico" 🔬
        - Pubblicazioni scientifiche, riviste scientifiche → "scientifico" 🔬
        - Tecnologia, software, AI → "tecnologico" 💻
        - Politica, governo, elezioni → "politico" 🏛️
        - Economia, finanza, mercati → "economico" 💰
        - Eventi, incidenti, meteo → "cronaca" 📰
        
        PRIORITÀ: Se la notizia menziona uno "studio" o una "ricerca", DEVE essere classificata come "scientifico" 🔬
        
        Restituisci solo il nome del dominio: "politico", "tecnologico", "scientifico", "economico", o "cronaca"
        """
        
        try:
            response = self.ai_provider.generate(prompt, max_tokens=50)
            domain = response.strip().lower()
            
            if domain in self.agents:
                return domain
            else:
                return self._fallback_domain_detection(article)
                
        except Exception as e:
            return self._fallback_domain_detection(article)
    
    def _fallback_domain_detection(self, article):
        """Rilevamento dominio di fallback basato su parole chiave"""
        
        text = f"{article.get('title', '')} {article.get('content', '')}".lower()
        

        if 'studio' in text or 'ricerca' in text or 'scienziati' in text or 'ricercatori' in text:
            return 'scientifico'
        

        keywords = {
            'politico': ['governo', 'politica', 'elezioni', 'ministro', 'parlamento', 'legge', 'meloni', 'cpi', 'partito', 'coalizione', 'opposizione', 'sinistra', 'destra', 'denuncia', 'accusa', 'zelensky', 'putin', 'ucraina', 'russia', 'guerra', 'conflitto', 'diplomazia', 'incontro', 'negoziati', 'presidente', 'capo stato'],
            'tecnologico': ['tecnologia', 'ai', 'intelligenza artificiale', 'startup', 'software', 'app', 'computer', 'digitale', 'innovazione', 'gadget'],
            'scientifico': ['studio', 'ricerca', 'scienza', 'medicina', 'università', 'laboratorio', 'scoperta', 'esperimento', 'pubblicazione', 'sindone', 'archeologia', 'storia'],
            'economico': ['economia', 'finanza', 'mercato', 'borsa', 'pil', 'inflazione', 'crisi', 'recessione', 'crescita', 'investimenti'],
            'cronaca': ['incidente', 'polizia', 'carabinieri', 'evento', 'cronaca', 'testimonianza', 'omicidio', 'rapina', 'terremoto', 'meteo', 'clima', 'caldo', 'freddo', 'pioggia', 'neve', 'tempesta', 'alluvione', 'siccità', 'ondata', 'anticiclone', 'previsioni', 'temperatura']
        }
        
        scores = {}
        for domain, words in keywords.items():
            scores[domain] = sum(1 for word in words if word in text)
        
        if max(scores.values()) > 0:
            return max(scores, key=scores.get)
        else:
            return 'cronaca'  # Default
    
    def get_agent(self, domain):
        """Ottiene l'agente per il dominio specificato"""
        return self.agents.get(domain, self.universal_agent)
    
    def execute_verification(self, article, analysis, language='it'):
        """Esegue la verifica completa con l'agente appropriato"""
        

        domain = self.detect_domain(article, analysis)
        
        if domain == 'scientifico':
            agent = self.agents['scientifico']
        else:
            agent = self.universal_agent
        

        queries = agent.generate_search_queries(article, analysis, language)
        
        try:
            settings = load_settings()
            serpapi_key = settings.get('serpapi_key')
            
            if serpapi_key:
                serpapi = SerpAPIIntegration(serpapi_key)
                

                all_results = []
                for query in queries[:3]: 
                    try:
 
                        news_results = serpapi.search_news(query, language, 3)
                        general_results = serpapi.search(query, language, 2)
                        
                        all_results.extend(news_results)
                        all_results.extend(general_results)
                        
                    except Exception as e:
                        continue
                
                if all_results:
                    results_text = []
                    for result in all_results[:10]:  # Massimo 10 risultati
                        results_text.append(f"Titolo: {result.get('title', 'N/A')}")
                        results_text.append(f"Fonte: {result.get('source', 'N/A')}")
                        results_text.append(f"Contenuto: {result.get('snippet', 'N/A')[:200]}...")
                        if result.get('date'):
                            results_text.append(f"Data: {result.get('date', 'N/A')}")
                        results_text.append("---")
                    
                    results = "\n".join(results_text)
                else:
                    results = "Nessun risultato trovato"
            else:
                results = "Chiave SerpAPI non configurata"
                
        except Exception as e:
            results = "Errore nel sistema di ricerca"
        

        evaluation = agent.evaluate_results(queries, results, language, None, article)
        
        return {
            'domain': domain,
            'agent': agent.specialization,
            'queries': queries,
            'evaluation': evaluation
        }
    
    def _get_search_type_for_domain(self, domain):
        """Determina il tipo di ricerca per dominio"""
        search_types = {
            'politico': 'ricerca politica',
            'tecnologico': 'ricerca tecnologica',
            'scientifico': 'ricerca scientifica',
            'economico': 'ricerca economica',
            'cronaca': 'ricerca cronaca'
        }
        return search_types.get(domain, 'ricerca generale') 