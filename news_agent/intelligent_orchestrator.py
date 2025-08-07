
from .settings import load_settings
from .ai_providers import create_ai_provider
from .specialized_agents import ScientificAgent, PoliticalAgent, TechnologyAgent, EconomicAgent, UniversalAgent
import json
import re

class IntelligentOrchestrator:
    """Orchestratore intelligente che usa LLM per decidere quale agente attivare"""
    
    def __init__(self):
        self.settings = load_settings()
        self.ai_provider = create_ai_provider(self.settings.get('provider', 'ollama'), self.settings)
        
        self.agents = {
            'scientifico': ScientificAgent(self.ai_provider),
            'politico': PoliticalAgent(self.ai_provider),
            'tecnologico': TechnologyAgent(self.ai_provider),
            'economico': EconomicAgent(self.ai_provider),
            'universale': UniversalAgent(self.ai_provider)
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
    
    def analyze_and_route(self, article, analysis, language='it'):
        
        prompt = f"""
        Sei un orchestratore intelligente. Analizza questa notizia e decidi quali agenti specializzati sono più adatti per verificarla.

        NOTIZIA:
        Titolo: {article.get('title', 'N/A')}
        Contenuto: {article.get('content', article.get('summary', 'N/A'))}
        Fonte: {article.get('source', 'N/A')}
        
        ANALISI CRITICA INIZIALE:
        {analysis}
        
        AGENTI DISPONIBILI:
        1. 🔬 SCIENTIFICO: Per notizie che riguardano studi, ricerche, scoperte scientifiche, pubblicazioni scientifiche, analisi di laboratorio, reperti storici, archeologia, medicina, scoperte archeologiche
        2. 🏛️ POLITICO: Per notizie che riguardano politica, governo, elezioni, diplomazia, leggi, istituzioni, dichiarazioni politiche
        3. 💻 TECNOLOGICO: Per notizie che riguardano tecnologia, AI, startup, innovazioni digitali, software
        4. 💰 ECONOMICO: Per notizie che riguardano economia, finanza, mercati, business, PIL, inflazione
        5. 🌍 UNIVERSALE: Per notizie di cronaca generale, eventi, notizie che non rientrano nelle categorie specifiche
        
        COMPITO:
        Analizza attentamente il CONTENUTO e il CONTESTO della notizia. 
        
        RAGIONAMENTO:
        - Che tipo di argomento tratta questa notizia?
        - Quali sono le fonti e le informazioni presentate?
        - Qual è la natura principale della notizia?
        - Che tipo di verifica richiede?
        - La notizia tocca più ambiti? (es. studio scientifico approvato dal governo = SCIENTIFICO + POLITICO)
        - È una notizia che riguarda la scienza, la politica, la tecnologia, l'economia o è una notizia generale?
        - IMPORTANTE: Per notizie scientifiche (studi, ricerche, scoperte) usa sempre SCIENTIFICO + UNIVERSALE
        - IMPORTANTE: Per notizie complesse (Sindone, reperti storici, scoperte archeologiche) usa sempre SCIENTIFICO + UNIVERSALE
        - IMPORTANTE: L'agente SCIENTIFICO deve valutare la METODOLOGIA, non solo l'autorevolezza
        - IMPORTANTE: Cerca limitazioni come ricostruzioni 3D, software gratuiti, mancanza di accesso diretto
        
        SELEZIONE AGENTI:
        - SEMPRE scegli MINIMO 2 agenti per una verifica più robusta e affidabile
        - Se la notizia è complessa e tocca più ambiti, scegli 2-3 agenti
        - Se la notizia è semplice, scegli comunque 2 agenti complementari
        - Gli agenti collaboreranno per fornire una verifica più accurata e bilanciata
        - Esempi: 🔬 SCIENTIFICO + 🌍 UNIVERSALE, 🏛️ POLITICO + 💰 ECONOMICO, 💻 TECNOLOGICO + 🔬 SCIENTIFICO
        
        ESTRATTORE DI INFORMAZIONI:
        Estrai informazioni specifiche che aiuteranno gli agenti scelti:
        
        - Per 🔬 SCIENTIFICO: autori, studi, riviste, metodologie, scoperte, report, strumenti utilizzati, accesso ai dati, controlli sperimentali
        - Per 🏛️ POLITICO: politici, istituzioni, dichiarazioni, eventi politici
        - Per 💻 TECNOLOGICO: aziende, tecnologie, innovazioni, brevetti, report
        - Per 💰 ECONOMICO: indicatori, dati, aziende, mercati, report
        - Per 🌍 UNIVERSALE: eventi, luoghi, persone, fatti principali
        
        Restituisci SOLO un JSON valido senza testo aggiuntivo:
        {{
            "agenti_scelti": ["scientifico", "politico", "tecnologico", "economico", "universale"],
            "motivazione": "Breve spiegazione",
            "caratteristiche_notizia": ["car1", "car2"],
            "livello_confidenza": 5,
            "strategia_collaborazione": "Breve strategia",
            "informazioni_specifiche": {{
                "entita_principali": ["ent1", "ent2"],
                "eventi_chiave": ["ev1", "ev2"],
                "fonti_citate": ["fonte1", "fonte2"],
                "dettagli_rilevanti": ["det1", "det2"]
            }}
        }}
        """
        
        try:
            response = self.ai_provider.generate(prompt, max_tokens=400)
            
            try:
                decision = json.loads(response)
            except json.JSONDecodeError as json_error:
                import re
                
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    try:
                        decision = json.loads(json_match.group())
                    except:
                        pass
                
                agents_match = re.search(r'"agenti_scelti":\s*\[([^\]]+)\]', response)
                if agents_match:
                    agents_str = agents_match.group(1)
                    agents = [agent.strip().strip('"').lower() for agent in agents_str.split(',')]
                    decision = {
                        "agenti_scelti": agents,
                        "motivazione": "JSON riparato",
                        "caratteristiche_notizia": [],
                        "livello_confidenza": 5,
                        "strategia_collaborazione": "Verifica collaborativa",
                        "informazioni_specifiche": {
                            "entita_principali": [],
                            "eventi_chiave": [],
                            "fonti_citate": [],
                            "dettagli_rilevanti": []
                        }
                    }
                
                decision = {
                    "agenti_scelti": ["scientifico", "universale"],
                    "motivazione": "Fallback per errore JSON",
                    "caratteristiche_notizia": [],
                    "livello_confidenza": 5,
                    "strategia_collaborazione": "Verifica collaborativa",
                    "informazioni_specifiche": {
                        "entita_principali": [],
                        "eventi_chiave": [],
                        "fonti_citate": [],
                        "dettagli_rilevanti": []
                    }
                }
            
            agents_chosen = decision.get('agenti_scelti', ['universale'])
            if isinstance(agents_chosen, str):
                agents_chosen = [agents_chosen]
            
            agents_chosen = [agent.lower() for agent in agents_chosen]
            
            if len(agents_chosen) < 2:
                if 'scientifico' in agents_chosen:
                    agents_chosen.append('universale')
                elif 'politico' in agents_chosen:
                    agents_chosen.append('universale')
                elif 'tecnologico' in agents_chosen:
                    agents_chosen.append('universale')
                elif 'economico' in agents_chosen:
                    agents_chosen.append('universale')
                else:
                    agents_chosen.append('scientifico')
            
            all_results = []
            agents_used = []
            
            for i, agent_name in enumerate(agents_chosen[:3], 1):
                agent = self.agents.get(agent_name, self.agents['universale'])
                agent_info = self._extract_agent_specific_info(decision, article, analysis, agent_name)
                result = self._execute_verification(agent, article, analysis, language, agent_info)
                
                all_results.append({
                    'agent': agent_name,
                    'result': result
                })
                agents_used.append(agent_name)
            
            verification_result = self._combine_agent_results(all_results, decision)
            verification_result['agents_used'] = agents_used
            verification_result['orchestrator_decision'] = decision
            
            return verification_result
            
        except Exception as e:
            return self._execute_verification(self.agents['universale'], article, analysis, language, None)
    
    def _extract_agent_specific_info(self, decision, article, analysis, agent_name):
        
        specific_info = decision.get('informazioni_specifiche', {})
        
        agent_info = {
            'agent_type': agent_name,
            'entita_principali': specific_info.get('entita_principali', []),
            'eventi_chiave': specific_info.get('eventi_chiave', []),
            'fonti_citate': specific_info.get('fonti_citate', []),
            'dettagli_rilevanti': specific_info.get('dettagli_rilevanti', [])
        }
        
        if agent_name == 'scientifico':
            agent_info.update(self._extract_scientific_info(decision, article, analysis))
        elif agent_name == 'politico':
            agent_info.update(self._extract_political_info(decision, article, analysis))
        elif agent_name == 'tecnologico':
            agent_info.update(self._extract_technology_info(decision, article, analysis))
        elif agent_name == 'economico':
            agent_info.update(self._extract_economic_info(decision, article, analysis))
        elif agent_name == 'universale':
            agent_info.update(self._extract_universal_info(decision, article, analysis))
        
        return agent_info
    
    def _extract_scientific_info(self, decision, article, analysis):
        return self._extract_study_info_from_decision(decision, article, analysis)
    
    def _extract_political_info(self, decision, article, analysis):
        content = f"{article.get('title', '')} {article.get('content', '')} {analysis}"
        content_lower = content.lower()
        
        political_info = {
            'politici_coinvolti': [],
            'istituzioni': [],
            'dichiarazioni': [],
            'eventi_politici': []
        }
        
        politician_patterns = [
            r'(\w+\s+\w+)\s+(?:presidente|ministro|sindaco|governatore)',
            r'(?:presidente|ministro|sindaco|governatore)\s+(\w+\s+\w+)',
            r'(\w+\s+\w+)\s+ha\s+dichiarato',
            r'dichiarazione\s+di\s+(\w+\s+\w+)'
        ]
        
        for pattern in politician_patterns:
            match = re.search(pattern, content_lower)
            if match:
                politician = match.group(1).strip().title()
                if len(politician.split()) >= 2:
                    political_info['politici_coinvolti'].append(politician)
        
        institution_patterns = [
            r'(?:governo|parlamento|senato|camera|ministero|comune|regione)',
            r'(?:partito|coalizione|opposizione)',
            r'(?:commissione|consiglio|assemblea)'
        ]
        
        for pattern in institution_patterns:
            matches = re.findall(pattern, content_lower)
            political_info['istituzioni'].extend(matches)
        
        return political_info
    
    def _extract_technology_info(self, decision, article, analysis):
        content = f"{article.get('title', '')} {article.get('content', '')} {analysis}"
        content_lower = content.lower()
        
        tech_info = {
            'aziende_tech': [],
            'tecnologie': [],
            'innovazioni': [],
            'brevetti': []
        }
        
        company_patterns = [
            r'(?:google|apple|microsoft|amazon|facebook|meta|tesla|netflix|uber|airbnb)',
            r'(\w+\s+\w+)\s+(?:inc|corp|tech|labs|ai|software)',
            r'(?:startup|azienda)\s+(\w+\s+\w+)'
        ]
        
        for pattern in company_patterns:
            matches = re.findall(pattern, content_lower)
            tech_info['aziende_tech'].extend(matches)
        
        tech_patterns = [
            r'(?:ai|intelligenza artificiale|machine learning|deep learning)',
            r'(?:blockchain|bitcoin|cryptocurrency|nft)',
            r'(?:cloud|cloud computing|saas|paas)',
            r'(?:5g|6g|internet of things|iot)',
            r'(?:virtual reality|vr|augmented reality|ar)'
        ]
        
        for pattern in tech_patterns:
            matches = re.findall(pattern, content_lower)
            tech_info['tecnologie'].extend(matches)
        
        return tech_info
    
    def _extract_economic_info(self, decision, article, analysis):
        content = f"{article.get('title', '')} {article.get('content', '')} {analysis}"
        content_lower = content.lower()
        
        economic_info = {
            'indicatori_economici': [],
            'aziende': [],
            'mercati': [],
            'dati_finanziari': []
        }
        
        indicator_patterns = [
            r'(?:pil|gdp|inflazione|inflazione|disoccupazione|tasso di interesse)',
            r'(?:borsa|ftse|nasdaq|dow jones|s&p 500)',
            r'(?:euro|dollaro|sterlina|yen|yuan)',
            r'(?:debito pubblico|deficit|surplus|bilancio)'
        ]
        
        for pattern in indicator_patterns:
            matches = re.findall(pattern, content_lower)
            economic_info['indicatori_economici'].extend(matches)
        
        return economic_info
    
    def _extract_universal_info(self, decision, article, analysis):
        content = f"{article.get('title', '')} {article.get('content', '')} {analysis}"
        content_lower = content.lower()
        
        universal_info = {
            'luoghi': [],
            'date': [],
            'persone': [],
            'fatti_principali': []
        }
        
        location_patterns = [
            r'(?:a|in|da|per)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'(?:città|paese|stato|regione|provincia)\s+di\s+([A-Z][a-z]+)'
        ]
        
        for pattern in location_patterns:
            matches = re.findall(pattern, content_lower)
            universal_info['luoghi'].extend(matches)
        
        return universal_info
    
    def _extract_study_info_from_decision(self, decision, article, analysis):
        
        content = f"{article.get('title', '')} {article.get('content', '')} {analysis}"
        content_lower = content.lower()
        
        study_info = {
            'study_name': None,
            'author_name': None,
            'journal': None,
            'keywords': []
        }
        
        author_patterns = [
            r'(\w+\s+\w+)\s+studio',
            r'studio\s+di\s+(\w+\s+\w+)',
            r'(\w+\s+\w+)\s+pubblicazione',
            r'pubblicazione\s+di\s+(\w+\s+\w+)',
            r'(\w+\s+\w+)\s+ricerca',
            r'ricerca\s+di\s+(\w+\s+\w+)',
            r'(\w+\s+\w+)\s+paper',
            r'paper\s+di\s+(\w+\s+\w+)',
            r'(\w+\s+\w+)\s+ha\s+scoperto',
            r'(\w+\s+\w+)\s+ha\s+trovato',
            r'(\w+\s+\w+)\s+ha\s+dimostrato'
        ]
        
        for pattern in author_patterns:
            match = re.search(pattern, content_lower)
            if match:
                potential_author = match.group(1).strip().title()
                if len(potential_author.split()) >= 2:
                    study_info['author_name'] = potential_author
                    break
        
        study_patterns = [
            r'studio\s+(?:su|sulla|sul)\s+([^,\.]+)',
            r'ricerca\s+(?:su|sulla|sul)\s+([^,\.]+)',
            r'pubblicazione\s+(?:su|sulla|sul)\s+([^,\.]+)',
            r'paper\s+(?:su|sulla|sul)\s+([^,\.]+)',
            r'(\w+(?:\s+\w+)*)\s+(?:è|sono)\s+stati\s+studiati',
            r'(\w+(?:\s+\w+)*)\s+(?:è|sono)\s+stati\s+analizzati'
        ]
        
        for pattern in study_patterns:
            match = re.search(pattern, content_lower)
            if match:
                study_name = match.group(1).strip()
                if len(study_name.split()) >= 2:  # Almeno 2 parole
                    study_info['study_name'] = study_name.title()
                    break
        
        journal_patterns = [
            r'pubblicato\s+(?:su|in)\s+([A-Za-z\s]+)',
            r'pubblicazione\s+(?:su|in)\s+([A-Za-z\s]+)',
            r'rivista\s+([A-Za-z\s]+)',
            r'journal\s+([A-Za-z\s]+)',
            r'([A-Za-z\s]+)\s+journal',
            r'([A-Za-z\s]+)\s+review'
        ]
        
        for pattern in journal_patterns:
            match = re.search(pattern, content_lower)
            if match:
                journal = match.group(1).strip().title()
                if len(journal.split()) >= 1:
                    study_info['journal'] = journal
                    break
        
        keywords = ['studio', 'ricerca', 'pubblicazione', 'paper', 'metodologia', 'risultati', 'scoperta', 'analisi', 'esperimento', 'test']
        study_info['keywords'] = [kw for kw in keywords if kw in content_lower]
        
        return study_info
    
    def _combine_agent_results(self, all_results, decision):
        
        if len(all_results) == 1:
            return all_results[0]['result']
        
        combined_queries = []
        combined_evidences_for = []
        combined_evidences_against = []
        combined_explanations = []
        
        for result_data in all_results:
            agent_name = result_data['agent']
            result = result_data['result']
            
            if 'queries' in result:
                combined_queries.extend([f"[{agent_name.upper()}] {query}" for query in result['queries']])
            
            if 'evaluation' in result:
                eval_data = result['evaluation']
                combined_evidences_for.extend([f"[{agent_name.upper()}] {evidence}" for evidence in eval_data.get('evidenze_a_favore', [])])
                combined_evidences_against.extend([f"[{agent_name.upper()}] {evidence}" for evidence in eval_data.get('evidenze_contro', [])])
                combined_explanations.append(f"[{agent_name.upper()}] {eval_data.get('spiegazione', 'N/A')}")
        
        total_confidence = 0
        total_agents = len(all_results)
        
        for result_data in all_results:
            if 'evaluation' in result_data['result']:
                total_confidence += result_data['result']['evaluation'].get('livello_affidabilita', 5)
        
        combined_confidence = total_confidence / total_agents if total_agents > 0 else 5
        
        confirmations = 0
        for result_data in all_results:
            if 'evaluation' in result_data['result']:
                if result_data['result']['evaluation'].get('conferma', False):
                    confirmations += 1
        
        final_confirmation = confirmations > total_agents / 2
        
        combined_evaluation = {
            'conferma': final_confirmation,
            'evidenze_a_favore': combined_evidences_for,
            'evidenze_contro': combined_evidences_against,
            'livello_affidabilita': round(combined_confidence, 1),
            'spiegazione': f"Verifica collaborativa di {total_agents} agenti:\n" + "\n".join(combined_explanations)
        }
        
        return {
            'domain': 'collaborativo',
            'agent': 'collaborativo',
            'queries': combined_queries,
            'evaluation': combined_evaluation,
            'collaborative_results': all_results
        }
    
    def _execute_verification(self, agent, article, analysis, language='it', agent_info=None):
        
        queries = agent.generate_search_queries(article, analysis, language)
        
        try:
            import time
            from .scrapingdog_integration import ScrapingDogIntegration
            settings = load_settings()
            scrapingdog_key = settings.get('scrapingdog_api_key')
            
            if scrapingdog_key:
                scrapingdog = ScrapingDogIntegration(scrapingdog_key)
                all_results = []
                
                for i, query in enumerate(queries[:2], 1):
                    try:
                        if i > 1:
                            time.sleep(1)
                        
                        news_results = scrapingdog.search_news(query, language, 2)
                        time.sleep(0.5)
                        general_results = scrapingdog.search(query, language, 1)
                        
                        all_results.extend(news_results)
                        all_results.extend(general_results)
                        
                    except Exception as e:
                        continue
                
                if all_results:
                    results_text = []
                    
                    for i, result in enumerate(all_results[:6], 1):
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
                results = "Chiave ScrapingDog non configurata"
                
        except Exception as e:
            results = "Errore nel sistema di ricerca"
        
        if agent_info:
            evaluation = agent.evaluate_results(queries, results, language, agent_info, article)
        else:
            evaluation = agent.evaluate_results(queries, results, language, None, article)
        
        return {
            'domain': agent.specialization,
            'agent': agent.specialization,
            'queries': queries,
            'evaluation': evaluation
        } 