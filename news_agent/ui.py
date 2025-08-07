
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

def show_table(articles, page, per_page, selected_idx=None):
    os.system('clear' if os.name == 'posix' else 'cls')
    table = Table(title=f"[bold blue]📰 Notizie da Multiple Fonti (Pagina {page})[/bold blue]")
    table.add_column("#", justify="center", style="bold red", no_wrap=True)
    table.add_column("Data", style="bold yellow", no_wrap=True)
    table.add_column("Fonte", style="bold yellow", no_wrap=True)
    table.add_column("Titolo", style="bold white")
    start = (page - 1) * per_page
    end = start + per_page
    for i, article in enumerate(articles[start:end], start=start):
        style = "bold white on blue" if selected_idx == i else ("none" if i % 2 == 0 else "dim")
        source = article.get('source', 'Sconosciuto')
        table.add_row(str(i), article['date'][:16], source, article['title'], style=style)
    console = Console()
    console.print(table)
    
    commands = "Comandi: ↑↓=naviga, Invio=apri articolo, n=avanti, p=indietro, [0-9]=seleziona articolo, o=apri link browser, v=analisi critica, c=configurazione, q=esci"
    console.print(f"[i]{commands}[/i]")

def show_article(article):
    os.system('clear' if os.name == 'posix' else 'cls')
    
    content = article.get('content', article.get('summary', 'Contenuto non disponibile'))
    
    article_panel = Panel(
        f"[bold blue]{article['title']}[/bold blue]\n\n"
        f"[dim]{article['date']}[/dim] [cyan]{article['author']}[/cyan]\n\n"
        f"{content}\n\n"
        f"[link={article['link']}]Leggi su Google News (premi 'o' per aprire)[/link]",
        title="[bold green]Articolo dettagliato[/bold green]"
    )
    Console().print(article_panel)

def show_verification_menu():
    """Mostra il menu di verifica semplificato"""
    console = Console()
    console.clear()
    console.print(Panel.fit(
        "[bold blue]🔍 ANALISI[/bold blue]\n\n"
        "[bold]Scegli cosa analizzare:[/bold]\n"
        "1. [bold]Articolo selezionato[/bold] - Analizza l'articolo corrente\n"
        "2. [bold]Testo personalizzato[/bold] - Inserisci un testo da analizzare\n"
        "3. [bold]URL articolo[/bold] - Inserisci un link da analizzare\n"
        "0. Torna indietro\n\n"
        "[yellow]Come funziona:[/yellow]\n"
        "• L'AI ragiona come un analista esperto\n"
        "• Rileva automaticamente il dominio e attiva l'agente specializzato:\n"
        "  🔬 Scientifico - per studi e ricerche\n"
        "  🏛️ Politico - per politica e governo\n"
        "  💻 Tecnologico - per tecnologia e AI\n"
        "  💰 Economico - per economia e finanza\n"
        "  🌍 Universale - per notizie generali\n"
        "• Genera query strategiche e valuta i risultati\n"
        "• Fornisce un giudizio finale basato su evidenze\n",
        title="[bold cyan]🧠 News Analyst[/bold cyan]"
    ))
    
    while True:
        try:
            choice = console.input("\nSeleziona opzione (0-3): ").strip()
            if choice == "0":
                return None
            elif choice in ["1", "2", "3"]:
                return choice
            else:
                console.print("[red]Opzione non valida. Riprova.[/red]")
        except KeyboardInterrupt:
            return None

def show_verification_results(analysis_result, model_name=None):
    """Mostra i risultati dell'analisi"""
    os.system('clear' if os.name == 'posix' else 'cls')
    console = Console()
    
<<<<<<< HEAD
    title = "[bold green]🧠 Analisi[/bold green]"
    if model_name:
        title += f" - {model_name}"
=======

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
>>>>>>> main
    
    console.print(Panel(
        analysis_result,
        title=title
    ))
    
    console.input("\nPremi invio per tornare alla lista...")

def get_custom_text():
    """Chiede all'utente di inserire un testo personalizzato da verificare"""
    console = Console()
    console.print("\n[bold yellow]📝 Inserisci il testo da verificare:[/bold yellow]")
    console.print("(Scrivi il testo e premi invio, oppure premi invio senza testo per annullare)")
    
    text = console.input("Testo: ").strip()
    return text

def get_article_url():
    """Chiede all'utente di inserire un URL di articolo da analizzare"""
    console = Console()
    console.print("\n[bold yellow]🔗 Inserisci l'URL dell'articolo da analizzare:[/bold yellow]")
    console.print("(Incolla il link e premi invio, oppure premi invio senza URL per annullare)")
    
    url = console.input("URL: ").strip()
    return url

def show_scraped_article(article):
    """Mostra l'articolo estratto in una finestra con bordi"""
    console = Console()
    console.clear()
    
    content = clean_ansi_content(article.get('content', ''))
    
    preview = content[:500] + "..." if len(content) > 500 else content
    
    article_text = f"""
[bold blue]{article.get('title', 'Titolo non disponibile')}[/bold blue]

[dim]📅 Data: {article.get('date', 'Non disponibile')}[/dim]
[dim]✍️ Autore: {article.get('author', 'Non disponibile')}[/dim]
[dim]📰 Fonte: {article.get('source', 'Non disponibile')}[/dim]
[dim]🔗 URL: {article.get('link', 'Non disponibile')}[/dim]

{'='*60}

[bold]PREVIEW DEL CONTENUTO:[/bold]
{preview}

{'='*60}

[dim]Contenuto completo: {len(content)} caratteri[/dim]
"""
    
    console.print(Panel(
        article_text,
        title="[bold green]📰 Articolo Estratto[/bold green]",
        padding=(1, 2)
    ))
    
    if len(content) > 500:
        console.clear()
        full_content = content[:3000] + "\n\n[... contenuto troncato ...]" if len(content) > 3000 else content
        
        full_article_text = f"""
[bold blue]{article.get('title', 'Titolo non disponibile')}[/bold blue]

[dim]📅 Data: {article.get('date', 'Non disponibile')}[/dim]
[dim]✍️ Autore: {article.get('author', 'Non disponibile')}[/dim]
[dim]📰 Fonte: {article.get('source', 'Non disponibile')}[/dim]

{'='*60}

{full_content}

{'='*60}
"""
        
        console.print(Panel(
            full_article_text,
            title="[bold green]📰 Contenuto Completo[/bold green]",
            padding=(1, 2)
        ))
        console.input("\nPremi invio per continuare...")

def show_analysis_animation(console):
    """Mostra un'animazione durante l'analisi"""
    console.print("\n[bold blue]🧠 Analisi in corso...[/bold blue]")
    console.print("[yellow]🔍 Verifica in corso, attendere...[/yellow]\n")

def clean_ansi_content(text):
    """Rimuove caratteri di controllo ANSI dal testo"""
    import re
    
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    text = ansi_escape.sub('', text)
    
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
    
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    
    return text.strip()

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
    """Modifica la chiave ScrapingDog"""
    console = Console()
    console.clear()
    
    console.print(Panel.fit(
        "[bold blue]🔍 CONFIGURAZIONE SCRAPINGDOG[/bold blue]\n\n"
        "ScrapingDog è necessario per la verifica delle notizie.\n"
        "Ottieni la tua chiave gratuita su: https://scrapingdog.com/\n\n"
        "[yellow]Chiave attuale:[/yellow]",
        title="Configurazione ScrapingDog",
        border_style="blue"
    ))
    
    try:
        from .settings import load_settings
        settings = load_settings()
        current_key = settings.get('scrapingdog_api_key', '')
        if current_key:
            console.print(f"[green]✅ Configurata: {current_key[:10]}...[/green]")
        else:
            console.print("[red]❌ Non configurata[/red]")
    except:
        console.print("[red]❌ Errore nel caricamento[/red]")
    
    console.print("\n[yellow]Inserisci la nuova chiave ScrapingDog (o premi invio per annullare):[/yellow]")
    new_key = console.input("Chiave: ").strip()
    
    if new_key:
        try:
            save_settings_change('scrapingdog_api_key', new_key)
            console.print("[green]✅ Chiave ScrapingDog salvata con successo![/green]")
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
    from .settings import load_settings
    
    console = Console()
    console.clear()
    
    settings = load_settings()
    per_page = settings.get('articles_per_page', '15')
    
    console.print(Panel.fit(
        "[bold blue]⚙️ IMPOSTAZIONI GENERALI[/bold blue]\n\n"
        "1. Lingua (it/en)\n"
        "2. Argomento RSS\n"
        "3. Articoli per pagina (attuale: {per_page})\n"
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
    
    provider = settings.get('provider', 'non impostato')
    provider_display = f"{provider.upper()}"
    
    model_display = "non impostato"
    if provider == 'ollama':
        model_display = settings.get('ollama_model', 'non impostato')
    elif provider == 'openai':
        model_display = settings.get('openai_model', 'non impostato')
    elif provider == 'claude':
        model_display = settings.get('claude_model', 'non impostato')
    
    settings_text = f"""
[bold blue]📋 CONFIGURAZIONE ATTUALE[/bold blue]

[bold green]🤖 AI CONFIGURATION[/bold green]
[bold]Provider Attivo:[/bold] {provider_display}
[bold]Modello Attivo:[/bold] {model_display}
[bold]URL Ollama:[/bold] {settings.get('ollama_url', 'non impostato')}

[bold yellow]🔑 API KEYS[/bold yellow]
[bold]OpenAI:[/bold] {'✅ Impostata' if settings.get('openai_api_key') else '❌ Non impostata'}
[bold]Claude:[/bold] {'✅ Impostata' if settings.get('claude_api_key') else '❌ Non impostata'}
[bold]SerpAPI:[/bold] {'✅ Impostata' if settings.get('serpapi_key') else '❌ Non impostata'}

[bold cyan]📰 NEWS CONFIGURATION[/bold cyan]
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
    
    default_section = {}
    ai_section = {}
    news_section = {}
    sources_section = {}
    
    ai_keys = ['provider', 'ollama_model', 'openai_model', 'claude_model', 
               'openai_api_key', 'claude_api_key', 'ollama_url']
    
    news_keys = ['lang', 'topic', 'articles_per_page', 'default_language', 
                 'enable_multilingual']
    

    
    sources_keys = ['quick_sources', 'default_output_language']
    
    for k, v in settings.items():
        if k in ai_keys:
            ai_section[k] = v
        elif k in news_keys:
            news_section[k] = v
        elif k in sources_keys:
            sources_section[k] = v
        else:
            default_section[k] = v
    
    if default_section:
        config['DEFAULT'] = default_section
    if ai_section:
        config['AI'] = ai_section
    if news_section:
        config['News'] = news_section
    if sources_section:
        config['Sources'] = sources_section
    
    settings_file = os.path.join(os.path.dirname(__file__), 'settings.ini')
    
    try:
        with open(settings_file, 'w') as f:
            config.write(f)
        return True
    except Exception as e:
        Console().print(f"[red]Errore nel salvataggio: {e}[/red]")
        return False
