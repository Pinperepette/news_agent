#!/usr/bin/env python

import os
import webbrowser
import sys
import select
import platform
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

def get_arrow_input():
    """Gestisce l'input con supporto per le frecce cross-platform"""
    console = Console()
    
    if platform.system() == "Windows":
        try:
            import msvcrt
            ch = msvcrt.getch()
            
            if ch in [b'\xe0', b'\x00']:
                ch2 = msvcrt.getch()
                # Codici per le frecce su Windows
                if ch2 == b'H':
                    return 'up'
                elif ch2 == b'P':
                    return 'down'
                elif ch2 == b'M':
                    return 'right'
                elif ch2 == b'K':
                    return 'left'
            
            return ch.decode('utf-8', errors='ignore').lower()
            
        except (ImportError, UnicodeDecodeError):

            return console.input().strip().lower()
    
    else:
        try:
            import tty
            import termios
            
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            
            try:
                tty.setraw(sys.stdin.fileno())
                
                ch = sys.stdin.read(1)

                if ch == '\x1b':
                    ch2 = sys.stdin.read(1)
                    if ch2 == '[':
                        ch3 = sys.stdin.read(1)
                        if ch3 == 'A':
                            return 'up'
                        elif ch3 == 'B':
                            return 'down'
                        elif ch3 == 'C':
                            return 'right'
                        elif ch3 == 'D':
                            return 'left'
                
                return ch.lower()
                
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                
        except (termios.error, OSError, AttributeError, ImportError):
            return console.input().strip().lower()

def show_table(articles, page, per_page, selected_idx=None, has_serpapi=False):
    os.system('clear' if os.name == 'posix' else 'cls')
    table = Table(title=f"Google News (Pagina {page})", border_style="green")
    table.add_column("#", justify="center", style="red", no_wrap=True)
    table.add_column("Data", style="yellow", no_wrap=True)
    table.add_column("Fonte", style="cyan", no_wrap=True)
    table.add_column("Titolo", style="white")
    start = (page - 1) * per_page
    end = start + per_page
    for i, article in enumerate(articles[start:end], start=start):
        style = "bold white on blue" if selected_idx == i else ("none" if i % 2 == 0 else "dim")
        table.add_row(str(i), article['date'][:16], article['author'], article['title'], style=style)
    console = Console()
    console.print(table)
    
    commands = "Comandi: ↑↓=naviga, Invio=apri articolo, n=avanti, p=indietro, numero=seleziona, o=apri link browser, s=sunto globale, a=agenti LLM, f=notizie successive, c=configurazione"

    if has_serpapi:
        commands += ", v=verifica"
    
    commands += ", q=esci"
    console.print(f"[i]{commands}[/i]")

def show_article(article):
    from .agents import get_article_full_content
    
    os.system('clear' if os.name == 'posix' else 'cls')
    
    content = get_article_full_content(article)
    
    article_panel = Panel(
        f"[bold]{article['title']}[/bold]\n\n"
        f"[dim]{article['date']}[/dim] [cyan]{article['author']}[/cyan]\n\n"
        f"{content}\n\n"
        f"[link={article['link']}]Leggi su Google News (premi 'o' per aprire)[/link]",
        title="Articolo dettagliato",
        border_style="white"
    )
    Console().print(article_panel)

def show_verification_menu():
    """Mostra il menu di verifica"""
    console = Console()
    console.clear()
    console.print(Panel.fit(
        "[bold blue]MENU VERIFICA[/bold blue]\n\n"
        "[bold]ARTICOLO SELEZIONATO:[/bold]\n"
        "1. Verifica standard\n"
        "2. Validazione verità standard\n"
        "3. Verifica multi-agente (sistema specializzato)\n"
        "4. Verifica multi-agente AUTOMATICA (scelta intelligente)\n\n"
        "[bold]TESTO PERSONALIZZATO:[/bold]\n"
        "5. Verifica standard\n"
        "6. Verifica avanzata (step-by-step)\n"
        "7. Validazione verità avanzata\n"
        "8. Verifica multi-agente AUTOMATICA\n"
        "0. Torna indietro\n\n"
        "[yellow]Modalità di ricerca:[/yellow]\n"
        "• [green]Veloce[/green]: 3 query, solo italiano, no scraping completo (~30s)\n"
        "• [yellow]Media[/yellow]: 5 query, bilingue, scraping completo (~2min)\n"
        "• [red]Grande[/red]: 10 query, bilingue, scraping completo (~5min)\n\n"
        "[cyan]Tipi di analisi:[/cyan]\n"
        "• [yellow]Standard[/yellow]: Analisi critica rapida (opzioni 1-2, 5-6)\n"
        "• [blue]Avanzata[/blue]: Ragionamento step-by-step dettagliato (opzioni 6-7)\n"
        "• [green]Multi-agente[/green]: Sistema specializzato con agenti collaborativi (opzioni 3-4, 8)\n"
        "• [magenta]AUTOMATICA[/magenta]: L'AI sceglie il tipo di analisi più appropriato (opzioni 4, 8)\n",
        title="🔍 Verifica Notizie",
        border_style="blue"
    ))
    
    while True:
        try:
            choice = console.input("\nSeleziona opzione (0-8): ").strip()
            if choice == "0":
                return None, None
            elif choice in ["1", "2", "3", "4", "5", "6", "7", "8"]:
                # Chiedi la modalità
                console.print("\n[yellow]Scegli modalità di ricerca:[/yellow]")
                console.print("1. [green]Veloce[/green] (~30 secondi)")
                console.print("2. [yellow]Media[/yellow] (~2 minuti)")
                console.print("3. [red]Grande[/red] (~5 minuti)")
                
                mode_choice = console.input("\nModalità (1-3, default=2): ").strip()
                
                if mode_choice == "1":
                    mode = "veloce"
                elif mode_choice == "3":
                    mode = "grande"
                else:
                    mode = "media"
                
                return choice, mode
            else:
                console.print("[red]Opzione non valida. Riprova.[/red]")
        except KeyboardInterrupt:
            return None, None

def show_verification_results(verification_data, agent_analysis=None, model_name=None):
    """Mostra i risultati della verifica"""
    os.system('clear' if os.name == 'posix' else 'cls')
    console = Console()
    

    if agent_analysis and "VERDETTO FINALE" in agent_analysis:

        parts = agent_analysis.split("VERDETTO FINALE:")
        if len(parts) > 1:
            analysis_part = parts[0].strip()
            verdict_part = "VERDETTO FINALE:" + parts[1].strip()
            
            title = "🤖 Analisi Sistema Multi-Agente"
            if model_name:
                title += f" - {model_name}"
            console.print(Panel(
                analysis_part,
                title=title,
                border_style="yellow"
            ))
            

            console.print(Panel(
                verdict_part,
                title="🎯 VERDETTO FINALE",
                border_style="red"
            ))
        else:

            title = "🤖 Analisi Sistema Multi-Agente"
            if model_name:
                title += f" - {model_name}"
            console.print(Panel(
                agent_analysis,
                title=title,
                border_style="yellow"
            ))
    else:

        console.print(Panel(
            verification_data.get('verification_summary', 'Nessun risultato'),
            title="📊 Risultati Verifica",
            border_style="cyan"
        ))
        
        if agent_analysis:
            title = "🤖 Analisi Agente LLM"
            if model_name:
                title += f" - {model_name}"
            console.print(Panel(
                agent_analysis,
                title=title,
                border_style="yellow"
            ))
    
    fact_check_results = verification_data.get('fact_check_results', [])
    if fact_check_results and not fact_check_results[0].get('error'):
        console.print("\n[bold green]🔗 Link Fact-Checking:[/bold green]")
        for i, result in enumerate(fact_check_results[:3], 1):
            console.print(f"{i}. {result.get('title', '')}")
            console.print(f"   Link: {result.get('link', '')}")
    
    reliable_results = verification_data.get('reliable_sources_results', [])
    if reliable_results and not reliable_results[0].get('error'):
        console.print("\n[bold blue]📰 Fonti Affidabili:[/bold blue]")
        for i, result in enumerate(reliable_results[:3], 1):
            console.print(f"{i}. {result.get('title', '')} ({result.get('source', '')})")
            console.print(f"   Link: {result.get('link', '')}")
    
    console.input("\nPremi invio per tornare alla lista...")

def get_custom_text():
    """Chiede all'utente di inserire un testo personalizzato da verificare"""
    console = Console()
    console.print("\n[bold yellow]📝 Inserisci il testo da verificare:[/bold yellow]")
    console.print("(Scrivi il testo e premi invio, oppure premi invio senza testo per annullare)")
    
    text = console.input("Testo: ").strip()
    return text

def show_settings_menu():
    """Mostra il menu di configurazione delle impostazioni"""
    console = Console()
    console.clear()
    
    console.print(Panel.fit(
        "[bold blue]⚙️ CONFIGURAZIONE IMPOSTAZIONI[/bold blue]\n\n"
        "1. Modifica provider AI (ollama/openai/claude)\n"
        "2. Modifica modello AI\n"
        "3. Modifica chiavi API\n"
        "4. Configura SerpAPI (verifica notizie)\n"
        "5. Modifica impostazioni generali\n"
        "6. Visualizza configurazione attuale\n"
        "0. Torna indietro\n\n"
        "[dim]Seleziona un'opzione:[/dim]",
        title="Menu Configurazione",
        border_style="blue"
    ))
    
    choice = console.input("Scelta: ").strip()
    return choice

def edit_ai_provider():
    """Modifica il provider AI"""
    console = Console()
    console.clear()
    
    console.print(Panel.fit(
        "[bold blue]🤖 SELEZIONE PROVIDER AI[/bold blue]\n\n"
        "1. Ollama (locale)\n"
        "2. OpenAI (GPT-4/GPT-3.5)\n"
        "3. Claude (Anthropic)\n"
        "4. Auto (fallback automatico)\n"
        "0. Torna indietro\n\n"
        "[dim]Scegli il provider da utilizzare:[/dim]",
        title="Provider AI",
        border_style="blue"
    ))
    
    choice = console.input("Scelta: ").strip()
    
    if choice == '1':
        return 'ollama'
    elif choice == '2':
        return 'openai'
    elif choice == '3':
        return 'claude'
    elif choice == '4':
        return 'auto'
    else:
        return None

def edit_ai_model(provider):
    """Modifica il modello AI per il provider selezionato"""
    console = Console()
    console.clear()
    
    if provider == 'ollama':
        console.print(Panel.fit(
            "[bold blue]🔧 MODELLO OLLAMA[/bold blue]\n\n"
            "Modelli disponibili:\n"
            "• qwen2:7b-instruct\n"
            "• llama3.2:3b-instruct\n"
            "• llama3.2:7b-instruct\n"
            "• llama3.2:8b-instruct\n"
            "• mistral:7b-instruct\n"
            "• codellama:7b-instruct\n\n"
            "[dim]Inserisci il nome del modello:[/dim]",
            title="Modello Ollama",
            border_style="blue"
        ))
        return console.input("Modello: ").strip()
    
    elif provider == 'openai':
        console.print(Panel.fit(
            "[bold blue]🔧 MODELLO OPENAI[/bold blue]\n\n"
            "Modelli disponibili:\n"
            "• gpt-4o\n"
            "• gpt-4o-mini\n"
            "• gpt-4-turbo\n"
            "• gpt-3.5-turbo\n\n"
            "[dim]Inserisci il nome del modello:[/dim]",
            title="Modello OpenAI",
            border_style="blue"
        ))
        return console.input("Modello: ").strip()
    
    elif provider == 'claude':
        console.print(Panel.fit(
            "[bold blue]🔧 MODELLO CLAUDE[/bold blue]\n\n"
            "Modelli disponibili:\n"
            "• claude-3-5-sonnet-20241022\n"
            "• claude-3-5-haiku-20241022\n"
            "• claude-3-opus-20240229\n"
            "• claude-3-sonnet-20240229\n\n"
            "[dim]Inserisci il nome del modello:[/dim]",
            title="Modello Claude",
            border_style="blue"
        ))
        return console.input("Modello: ").strip()
    
    return None

def edit_serpapi():
    """Modifica la chiave SerpAPI"""
    console = Console()
    console.clear()
    
    console.print(Panel.fit(
        "[bold blue]🔍 CONFIGURAZIONE SERPAPI[/bold blue]\n\n"
        "SerpAPI è necessaria per la verifica delle notizie.\n"
        "Ottieni la tua chiave gratuita su: https://serpapi.com/\n\n"
        "[yellow]Chiave attuale:[/yellow]",
        title="Configurazione SerpAPI",
        border_style="blue"
    ))
    
    try:
        from .settings import load_settings
        settings = load_settings()
        current_key = settings.get('serpapi_key', '')
        if current_key:
            console.print(f"[green]✅ Configurata: {current_key[:10]}...[/green]")
        else:
            console.print("[red]❌ Non configurata[/red]")
    except:
        console.print("[red]❌ Errore nel caricamento[/red]")
    
    console.print("\n[yellow]Inserisci la nuova chiave SerpAPI (o premi invio per annullare):[/yellow]")
    new_key = console.input("Chiave: ").strip()
    
    if new_key:
        try:
            save_settings_change('serpapi_key', new_key)
            console.print("[green]✅ Chiave SerpAPI salvata con successo![/green]")
            console.print("[yellow]Riavvia l'applicazione per applicare le modifiche.[/yellow]")
        except Exception as e:
            console.print(f"[red]❌ Errore nel salvataggio: {e}[/red]")
    else:
        console.print("[yellow]Operazione annullata.[/yellow]")
    
    console.input("\nPremi invio per tornare al menu...")

def edit_api_keys():
    """Modifica le chiavi API"""
    console = Console()
    console.clear()
    
    console.print(Panel.fit(
        "[bold blue]🔑 CHIAVI API[/bold blue]\n\n"
        "1. Chiave OpenAI\n"
        "2. Chiave Claude (Anthropic)\n"
        "3. Chiave SerpAPI\n"
        "4. URL Ollama\n"
        "0. Torna indietro\n\n"
        "[dim]Seleziona cosa modificare:[/dim]",
        title="Chiavi API",
        border_style="blue"
    ))
    
    choice = console.input("Scelta: ").strip()
    
    if choice == '1':
        console.print("\n[dim]Inserisci la chiave API di OpenAI:[/dim]")
        return ('openai_api_key', console.input("Chiave: ").strip())
    elif choice == '2':
        console.print("\n[dim]Inserisci la chiave API di Claude:[/dim]")
        return ('claude_api_key', console.input("Chiave: ").strip())
    elif choice == '3':
        console.print("\n[dim]Inserisci la chiave API di SerpAPI:[/dim]")
        return ('serpapi_key', console.input("Chiave: ").strip())
    elif choice == '4':
        console.print("\n[dim]Inserisci l'URL di Ollama (default: http://localhost:11434):[/dim]")
        return ('ollama_url', console.input("URL: ").strip())
    
    return None

def edit_general_settings():
    """Modifica le impostazioni generali"""
    console = Console()
    console.clear()
    
    console.print(Panel.fit(
        "[bold blue]⚙️ IMPOSTAZIONI GENERALI[/bold blue]\n\n"
        "1. Lingua (it/en)\n"
        "2. Argomento RSS\n"
        "3. Articoli per pagina\n"
        "0. Torna indietro\n\n"
        "[dim]Seleziona cosa modificare:[/dim]",
        title="Impostazioni Generali",
        border_style="blue"
    ))
    
    choice = console.input("Scelta: ").strip()
    
    if choice == '1':
        console.print("\n[dim]Inserisci la lingua (it/en):[/dim]")
        return ('lang', console.input("Lingua: ").strip())
    elif choice == '2':
        console.print("\n[dim]Inserisci l'argomento RSS (es: IT:it, US:en):[/dim]")
        return ('topic', console.input("Argomento: ").strip())
    elif choice == '3':
        console.print("\n[dim]Inserisci il numero di articoli per pagina:[/dim]")
        return ('articles_per_page', console.input("Numero: ").strip())
    
    return None

def show_current_settings():
    """Mostra la configurazione attuale"""
    from .settings import load_settings
    
    settings = load_settings()
    console = Console()
    console.clear()
    
    settings_text = f"""
[bold blue]📋 CONFIGURAZIONE ATTUALE[/bold blue]

[bold]Provider AI:[/bold] {settings.get('provider', 'non impostato')}
[bold]Modello Ollama:[/bold] {settings.get('ollama_model', 'non impostato')}
[bold]Modello OpenAI:[/bold] {settings.get('openai_model', 'non impostato')}
[bold]Modello Claude:[/bold] {settings.get('claude_model', 'non impostato')}
[bold]URL Ollama:[/bold] {settings.get('ollama_url', 'non impostato')}

[bold]Chiave OpenAI:[/bold] {'✅ Impostata' if settings.get('openai_api_key') else '❌ Non impostata'}
[bold]Chiave Claude:[/bold] {'✅ Impostata' if settings.get('claude_api_key') else '❌ Non impostata'}
[bold]Chiave SerpAPI:[/bold] {'✅ Impostata' if settings.get('serpapi_key') else '❌ Non impostata'}

[bold]Lingua:[/bold] {settings.get('lang', 'non impostata')}
[bold]Argomento:[/bold] {settings.get('topic', 'non impostato')}
[bold]Articoli per pagina:[/bold] {settings.get('articles_per_page', 'non impostato')}
"""
    
    console.print(Panel.fit(settings_text, title="Configurazione Attuale", border_style="green"))
    console.input("\nPremi invio per tornare indietro")

def save_settings_change(key, value):
    """Salva una modifica nelle impostazioni"""
    from .settings import load_settings
    import configparser
    import os
    
    settings = load_settings()
    settings[key] = value
    
    config = configparser.ConfigParser()
    config['DEFAULT'] = settings
    
    settings_file = os.path.join(os.path.dirname(__file__), 'settings.ini')
    
    try:
        with open(settings_file, 'w') as f:
            config.write(f)
        return True
    except Exception as e:
        Console().print(f"[red]Errore nel salvataggio: {e}[/red]")
        return False
