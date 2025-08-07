
from .settings import load_settings
from .ai_providers import create_ai_provider
from .intelligent_orchestrator import IntelligentOrchestrator
import json

class CriticalAnalyst:
    def __init__(self):
        self.settings = load_settings()
        self.ai_provider = create_ai_provider(self.settings.get('provider', 'ollama'), self.settings)
        self.orchestrator = IntelligentOrchestrator()
        
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
    
    def get_agents_display(self, agents_list):
        """Formatta la lista degli agenti con le loro icone"""
        if not agents_list:
            return "N/A"
        
        formatted_agents = []
        for agent in agents_list:
            icon = self.get_agent_icon(agent)
            formatted_agents.append(f"{icon} {agent.upper()}")
        
        return ", ".join(formatted_agents)
    
    def analyze_critically(self, article, language='it'):
        
        critical_analysis_prompt = f"""
        Sei un analista critico esperto di notizie. Analizza questa notizia con scetticismo professionale.
        
        NOTIZIA:
        Titolo: {article.get('title', 'N/A')}
        Contenuto: {article.get('content', article.get('summary', 'N/A'))}
        Fonte: {article.get('source', 'N/A')}
        Data: {article.get('date', 'N/A')}
        
        Esegui un'analisi critica in {language} considerando:
        
        1. VEROSIMIGLIANZA INTRINSECA:
        - La notizia è plausibile dal punto di vista logico?
        - Ci sono contraddizioni interne?
        - I fatti riportati sono coerenti con la realtà?
        
        2. CONTESTO E TIMING:
        - Il timing dell'annuncio è sospetto?
        - Ci sono eventi correlati che potrebbero spiegare la notizia?
        - È un periodo in cui simili notizie sono comuni?
        
        3. FONTE E CREDIBILITÀ:
        - La fonte è affidabile?
        - Ha una storia di accuratezza?
        - Potrebbe avere bias o interessi particolari?
        
        4. PUNTI SOSPETTI:
        - Quali elementi sembrano troppo belli per essere veri?
        - Ci sono dettagli vaghi o mancanti?
        - La notizia sembra clickbait?
        
        5. POSSIBILI SCENARI:
        - Se fosse vera, quali sarebbero le implicazioni?
        - Se fosse falsa, perché potrebbe essere stata pubblicata?
        - Ci sono spiegazioni alternative?
        
        Fornisci un'analisi strutturata in formato JSON:
        {{
            "verosimiglianza": "alta/media/bassa",
            "punti_sospetti": ["lista punti sospetti"],
            "possibili_scenari": ["scenario 1", "scenario 2"],
            "query_strategiche": ["query 1", "query 2"],
            "livello_credibilità": 1-10,
            "raccomandazioni": "suggerimenti per verificare"
        }}
        """
        
        try:
            response = self.ai_provider.generate(critical_analysis_prompt, max_tokens=800)
            
            try:
                analysis = json.loads(response)
            except json.JSONDecodeError:
                analysis = {
                    "verosimiglianza": "media",
                    "punti_sospetti": ["Impossibile parsare l'analisi"],
                    "possibili_scenari": ["Analisi non strutturata"],
                    "query_strategiche": ["Verifica fonte", "Cerca conferme"],
                    "livello_credibilità": 5,
                    "raccomandazioni": "Verifica manuale necessaria",
                    "analisi_grezza": response
                }
            
            verification_result = self.orchestrator.analyze_and_route(article, analysis, language)
            report = self.format_complete_report(analysis, verification_result, language)
            
            return report
            
        except Exception as e:
            error_report = f"""
{'='*60}
ERRORE ANALISI CRITICA
{'='*60}

Errore: {e}

ANALISI NON DISPONIBILE
Si consiglia verifica manuale della notizia.
"""
            return error_report
    
    def format_complete_report(self, analysis, verification_result, language='it'):
        
        domain = verification_result['domain']
        agent = verification_result['agent']
        queries = verification_result['queries']
        evaluation = verification_result['evaluation']
        
        report = f"""
{'='*70}
[bold blue]ANALISI COMPLETA DELLA NOTIZIA[/bold blue]
{'='*70}

[bold yellow]FASE 1: ANALISI INIZIALE[/bold yellow]
- Verosimiglianza: {analysis.get('verosimiglianza', 'N/A')}
- Livello credibilità: {analysis.get('livello_credibilità', 'N/A')}/10

[bold red]PUNTI SOSPETTI IDENTIFICATI:[/bold red]
"""
        
        for point in analysis.get('punti_sospetti', []):
            report += f"  - {point}\n"
        
        report += f"""
POSSIBILI SCENARI:
"""
        
        for scenario in analysis.get('possibili_scenari', []):
            report += f"  - {scenario}\n"
        
        agents_used = verification_result.get('agents_used', [agent])
        
        report += f"""
[bold green]FASE 2: VERIFICA SPECIALIZZATA[/bold green]
- Dominio rilevato: {domain.upper()}
"""
        
        if len(agents_used) > 1:
            agents_display = self.get_agents_display(agents_used)
            report += f"- Verifica collaborativa: {agents_display}\n"
            report += f"- Strategia: Collaborazione tra {len(agents_used)} agenti specializzati\n"
        else:
            agent_icon = self.get_agent_icon(agent)
            report += f"- Agente attivato: {agent_icon} {agent.upper()}\n"
        
        if 'orchestrator_decision' in verification_result:
            decision = verification_result['orchestrator_decision']
            agents_chosen = decision.get('agenti_scelti', [])
            agents_display = self.get_agents_display(agents_chosen)
            
            report += f"""
🧠 DECISIONE ORCHESTRATORE INTELLIGENTE:
- Agenti scelti: {agents_display}
- Motivazione: {decision.get('motivazione', 'N/A')}
- Livello confidenza: {decision.get('livello_confidenza', 'N/A')}/10
- Caratteristiche: {', '.join(decision.get('caratteristiche_notizia', []))}
"""
        
        agent_icon = self.get_agent_icon(agent)
        agent_name_upper = agent.upper()
        
        if agent == 'scientifico':
            report += f"""
[bold cyan]{agent_icon} AGENTE SCIENTIFICO ATTIVATO[/bold cyan]
- Analisi specializzata per studi e ricerche
- Ricerca di paper scientifici e pubblicazioni
- Valutazione di critiche e lacune metodologiche
- Verifica della qualità della ricerca

[bold magenta]QUERY STRATEGICHE GENERATE:[/bold magenta]
"""
        elif agent == 'politico':
            report += f"""
[bold blue]{agent_icon} AGENTE POLITICO ATTIVATO[/bold blue]
- Analisi specializzata per notizie politiche
- Verifica di dichiarazioni e fatti politici
- Controllo di fonti istituzionali e ufficiali

[bold magenta]QUERY STRATEGICHE GENERATE:[/bold magenta]
"""
        elif agent == 'tecnologico':
            report += f"""
[bold green]{agent_icon} AGENTE TECNOLOGICO ATTIVATO[/bold green]
- Analisi specializzata per notizie tecnologiche
- Verifica di innovazioni e startup
- Controllo di brevetti e sviluppi tech

[bold magenta]QUERY STRATEGICHE GENERATE:[/bold magenta]
"""
        elif agent == 'economico':
            report += f"""
[bold yellow]{agent_icon} AGENTE ECONOMICO ATTIVATO[/bold yellow]
- Analisi specializzata per notizie economiche
- Verifica di dati finanziari e indicatori
- Controllo di report economici e mercati

[bold magenta]QUERY STRATEGICHE GENERATE:[/bold magenta]
"""
        else:
            report += f"""
[bold white]{agent_icon} AGENTE {agent_name_upper} ATTIVATO[/bold white]
- Analisi generale e multidisciplinare
- Verifica di fonti multiple
- Controllo di fatti e contesto

[bold magenta]QUERY STRATEGICHE GENERATE:[/bold magenta]
"""
        
        for i, query in enumerate(queries, 1):
            report += f"  {i}. {query}\n"
        
        if evaluation:
            report += f"""
[bold orange]FASE 3: VALUTAZIONE FINALE[/bold orange]
- Conferma: {'SI' if evaluation.get('conferma', False) else 'NO'}
- Livello affidabilità: {evaluation.get('livello_affidabilita', 'N/A')}/10

[bold green]EVIDENZE A FAVORE:[/bold green]
"""
            
            for evidence in evaluation.get('evidenze_a_favore', []):
                report += f"  - {evidence}\n"
            
            report += f"""
[bold red]EVIDENZE CONTRO:[/bold red]
"""
            
            for evidence in evaluation.get('evidenze_contro', []):
                report += f"  - {evidence}\n"
            
            if 'collaborative_results' in verification_result and len(agents_used) > 1:
                collaborative_results = verification_result['collaborative_results']
                
                report += f"""
[bold cyan]RISULTATI DETTAGLIATI DELLA COLLABORAZIONE:[/bold cyan]
"""
                
                for result_data in collaborative_results:
                    agent_name = result_data['agent']
                    agent_icon = self.get_agent_icon(agent_name)
                    agent_name_upper = agent_name.upper()
                    eval_data = result_data['result']['evaluation']
                    
                    report += f"""
[bold yellow]{agent_icon} {agent_name_upper}:[/bold yellow]
- Conferma: {'SI' if eval_data.get('conferma', False) else 'NO'}
- Livello affidabilità: {eval_data.get('livello_affidabilita', 'N/A')}/10

[bold green]EVIDENZE A FAVORE ({agent_icon} {agent_name_upper}):[/bold green]
"""
                    
                    for evidence in eval_data.get('evidenze_a_favore', []):
                        report += f"  - {evidence}\n"
                    
                    report += f"""
[bold red]EVIDENZE CONTRO ({agent_icon} {agent_name_upper}):[/bold red]
"""
                    
                    for evidence in eval_data.get('evidenze_contro', []):
                        report += f"  - {evidence}\n"
            
            report += f"""
[bold white]SPIEGAZIONE DETTAGLIATA:[/bold white]
{evaluation.get('spiegazione', 'N/A')}
"""
        else:
            report += f"""
[bold orange]FASE 3: VALUTAZIONE FINALE[/bold orange]
- Conferma: NON DISPONIBILE
- Livello affidabilità: N/A

[bold red]IMPOSSIBILE VALUTARE I RISULTATI[/bold red]
- Il sistema non è riuscito a valutare i risultati delle ricerche
- La notizia potrebbe essere vera ma non verificabile automaticamente
- Si consiglia verifica manuale
"""
        
        report += f"""
{'='*70}
[bold purple]GIUDIZIO FINALE: {'VERA' if evaluation.get('conferma', False) else 'FALSA/INCONCLUSIVA'}[/bold purple]
{'='*70}
"""
        
        return report
    
    def generate_strategic_queries(self, analysis, language='it'):
        
        if 'query_strategiche' in analysis and analysis['query_strategiche']:
            return analysis['query_strategiche']
        
        points = analysis.get('punti_sospetti', [])
        
        query_prompt = f"""
        Basandoti sui punti sospetti identificati, genera 3-5 query strategiche per verificare la notizia.
        
        PUNTI SOSPETTI:
        {points}
        
        Genera query in {language} che:
        1. Verifichino la fonte ufficiale
        2. Cerchino conferme da fonti indipendenti
        3. Controllino il contesto temporale
        4. Verifichino fatti specifici menzionati
        
        Fornisci solo le query, una per riga:
        """
        
        try:
            response = self.ai_provider.generate(query_prompt, max_tokens=300)
            queries = [q.strip() for q in response.split('\n') if q.strip()]
            return queries[:5]
        except Exception as e:
            return [f"Verifica {analysis.get('verosimiglianza', 'la notizia')}"]
    
    def evaluate_verification_results(self, original_analysis, verification_data, language='it'):
        
        evaluation_prompt = f"""
        Valuta i risultati della verifica e fornisci un giudizio finale.
        
        ANALISI INIZIALE:
        {json.dumps(original_analysis, ensure_ascii=False, indent=2)}
        
        DATI DI VERIFICA:
        {json.dumps(verification_data, ensure_ascii=False, indent=2)}
        
        Fornisci una valutazione finale in {language} in formato JSON:
        {{
            "giudizio_finale": "VERA/FALSA/INCONCLUSIVA",
            "confidenza": 1-10,
            "evidenze_a_favore": ["evidenza 1", "evidenza 2"],
            "evidenze_contro": ["evidenza 1", "evidenza 2"],
            "spiegazione": "spiegazione dettagliata",
            "raccomandazioni_finali": "cosa fare ora"
        }}
        """
        
        try:
            response = self.ai_provider.generate(evaluation_prompt, max_tokens=600)
            
            try:
                evaluation = json.loads(response)
            except json.JSONDecodeError:
                evaluation = {
                    "giudizio_finale": "INCONCLUSIVA",
                    "confidenza": 5,
                    "evidenze_a_favore": ["Analisi non strutturata"],
                    "evidenze_contro": ["Verifica manuale necessaria"],
                    "spiegazione": response,
                    "raccomandazioni_finali": "Verifica manuale"
                }
            
            return evaluation
            
        except Exception as e:
            return {
                "giudizio_finale": "INCONCLUSIVA",
                "confidenza": 0,
                "evidenze_a_favore": [],
                "evidenze_contro": [f"Errore di sistema: {e}"],
                "spiegazione": "Impossibile valutare i risultati",
                "raccomandazioni_finali": "Verifica manuale necessaria"
            }
    
    def format_analysis_report(self, analysis, queries, evaluation, language='it'):
        """Formatta il report finale dell'analisi"""
        
        report = f"""
{'='*60}
ANALISI DELLA NOTIZIA
{'='*60}

ANALISI INIZIALE:
- Verosimiglianza: {analysis.get('verosimiglianza', 'N/A')}
- Livello credibilità: {analysis.get('livello_credibilità', 'N/A')}/10

PUNTI SOSPETTI:
"""
        
        for point in analysis.get('punti_sospetti', []):
            report += f"  - {point}\n"
        
        report += f"""
POSSIBILI SCENARI:
"""
        
        for scenario in analysis.get('possibili_scenari', []):
            report += f"  - {scenario}\n"
        
        report += f"""
QUERY STRATEGICHE GENERATE:
"""
        
        for i, query in enumerate(queries, 1):
            report += f"  {i}. {query}\n"
        
        report += f"""
RACCOMANDAZIONI:
{analysis.get('raccomandazioni', 'N/A')}
"""
        
        if evaluation:
            report += f"""
VALUTAZIONE FINALE:
- Giudizio: {evaluation.get('giudizio_finale', 'N/A')}
- Confidenza: {evaluation.get('confidenza', 'N/A')}/10

EVIDENZE A FAVORE:
"""
            
            for evidence in evaluation.get('evidenze_a_favore', []):
                report += f"  - {evidence}\n"
            
            report += f"""
EVIDENZE CONTRO:
"""
            
            for evidence in evaluation.get('evidenze_contro', []):
                report += f"  - {evidence}\n"
            
            report += f"""
SPIEGAZIONE:
{evaluation.get('spiegazione', 'N/A')}

RACCOMANDAZIONI:
{evaluation.get('raccomandazioni_finali', 'N/A')}
"""
        
        report += f"""
{'='*60}
"""
        
        return report 