
from .settings import load_settings
from .fetcher import fetch_articles, fetch_multiple_sources

from .critical_analyst import CriticalAnalyst
from .article_scraper import ArticleScraper
from .ui import show_table, show_article, get_arrow_input, show_verification_menu, show_verification_results, show_settings_menu, edit_ai_provider, edit_ai_model, edit_api_keys, edit_serpapi, edit_general_settings, show_current_settings, save_settings_change, get_custom_text, get_article_url, show_scraped_article, show_analysis_animation
from .ai_providers import create_ai_provider
from rich.panel import Panel
from rich.console import Console
import webbrowser
import sys

def get_model_name(ai_provider):
    """Ottiene il nome del modello dall'AI provider"""
    if hasattr(ai_provider, 'model'):
        return ai_provider.model
    return "Modello sconosciuto"

def handle_settings_menu(console):
    """Gestisce il menu delle impostazioni"""
    while True:
        choice = show_settings_menu()
        
        if choice == '0':
            break
        elif choice == '1':
            provider = edit_ai_provider()
            if provider and save_settings_change('provider', provider):
                console.print(f"[green]✅ Provider AI impostato su: {provider}[/green]")
                console.input("\nPremi invio per continuare...")
        elif choice == '2':
            from .settings import load_settings
            settings = load_settings()
            current_provider = settings.get('provider', 'ollama')
            
            if current_provider == 'auto':
                console.print("[yellow]⚠️ Impostazione 'auto' attiva. Seleziona prima un provider specifico.[/yellow]")
                console.input("\nPremi invio per continuare...")
                continue
            
            model = edit_ai_model(current_provider)
            if model:
                key = f'{current_provider}_model'
                if save_settings_change(key, model):
                    console.print(f"[green]✅ Modello {current_provider} impostato su: {model}[/green]")
                    console.input("\nPremi invio per continuare...")
        elif choice == '3':
            result = edit_api_keys()
            if result:
                key, value = result
                if save_settings_change(key, value):
                    console.print(f"[green]✅ {key} salvato con successo[/green]")
                    console.input("\nPremi invio per continuare...")
        elif choice == '4':
            edit_serpapi()
        elif choice == '5':
            result = edit_general_settings()
            if result:
                key, value = result
                if save_settings_change(key, value):
                    console.print(f"[green]✅ {key} impostato su: {value}[/green]")
                    console.input("\nPremi invio per continuare...")
        elif choice == '6':
            show_current_settings()
        else:
            console.print("[red]Opzione non valida[/red]")
            console.input("\nPremi invio per continuare...")

def main():
    settings = load_settings()
    
    lang = settings.get("lang", "it")
    topic = settings.get("topic")
    per_page = int(settings.get("articles_per_page", 15))
    provider = settings.get("provider", "ollama")
    serpapi_key = settings.get("serpapi_key")
    
    console = Console()
    

    
    try:
        ai_provider = create_ai_provider(provider, settings)
        model_name = get_model_name(ai_provider)
    except ValueError as e:
        console.print(f"[red]Errore configurazione AI: {e}[/red]")
        return
    
    critical_analyst = CriticalAnalyst()
    

    
    console.print("\n[bold yellow]📰 Caricamento notizie da multiple fonti...[/bold yellow]")
    
    articles = fetch_multiple_sources(max_articles_per_source=15)
    if not articles:
        console.print("[red]❌ Nessun articolo disponibile al momento[/red]")
        console.print("[dim]Riprova più tardi o verifica la connessione internet[/dim]")
        return
    
    current_page = 1
    total_pages = (len(articles) + per_page - 1) // per_page
    selected_idx = 0

    while True:
        show_table(articles, current_page, per_page, selected_idx)
        user_input = get_arrow_input()

        if user_input == 'q':
            break
        elif user_input in ['n', 'avanti'] and current_page < total_pages:
            current_page += 1
        elif user_input in ['p', 'indietro'] and current_page > 1:
            current_page -= 1
        elif user_input in ['up', 'w'] and selected_idx > 0:
            selected_idx -= 1
        elif user_input in ['down', 'z'] and selected_idx < len(articles) - 1:
            selected_idx += 1
        elif user_input == 'f':
            if selected_idx < len(articles) - 1:
                selected_idx += 1
            elif current_page < total_pages:
                current_page += 1
                selected_idx = 0
            else:
                console.print("[yellow]Sei già all'ultima notizia![/yellow]")
        elif user_input == 's':
            idx = selected_idx
            article = articles[idx]
            console.print(f"\n[bold yellow]📰 Analizzando: {article['title']}[/bold yellow]")
            console.print("[yellow]⚠️ Funzione sunto non più disponibile nel nuovo sistema[/yellow]")
            console.print("[blue]💡 Usa 'v' per analisi critica completa[/blue]")
            console.input("\nPremi invio per tornare alla lista")
        elif user_input == 'o':
            idx = selected_idx
            webbrowser.open(articles[idx]['link'])
            console.print(f"[bold green]Apro la notizia #{idx} nel browser...[/bold green]")
        elif user_input == 'a':
            idx = selected_idx
            article = articles[idx]
            show_article(article)
            console.print("\n[bold yellow]⚠️ Funzione agenti LLM non più disponibile nel nuovo sistema[/bold yellow]")
            console.print("[blue]💡 Usa 'v' per analisi critica completa con orchestratore intelligente[/blue]")
            console.input("\nPremi invio per tornare alla lista")
        elif user_input == 'v':
            result = show_verification_menu()
            
            if result is None:
                continue
            
            if result == '1':
                idx = selected_idx
                article = articles[idx]
                console.print(f"\n[bold blue]🧠 Analizzando articolo: {article['title']}[/bold blue]")
                
                try:
                    analysis = critical_analyst.analyze_critically(article, 'it')
                    show_verification_results(analysis, model_name)
                except Exception as e:
                    console.print(f"[red]❌ Errore analisi: {e}[/red]")
                    console.input("\nPremi invio per tornare alla lista")
            
            elif result == '2':
                custom_text = get_custom_text()
                if custom_text.strip():
                    console.print(f"\n[bold blue]🧠 Analizzando testo personalizzato...[/bold blue]")
                    
                    article = {
                        'title': 'Testo personalizzato',
                        'content': custom_text,
                        'source': 'input_utente'
                    }
                    
                    try:
                        analysis = critical_analyst.analyze_critically(article, 'it')
                        show_verification_results(analysis, model_name)
                    except Exception as e:
                        console.print(f"[red]❌ Errore analisi: {e}[/red]")
                        console.input("\nPremi invio per tornare alla lista")
            
            elif result == '3':
                url = get_article_url()
                if url.strip():
                    console.print(f"\n[bold blue]🔍 Scraping URL...[/bold blue]")
                    
                    try:
                        scraper = ArticleScraper()
                        
                        if not scraper.validate_url(url):
                            console.print("[yellow]⚠️ URL non riconosciuto come articolo di notizia, ma proverò comunque...[/yellow]")
                        
                        article = scraper.scrape_article(url)
                        
                        if article:
                            console.print(f"[green]✅ Articolo estratto con successo![/green]")
                            
                            show_scraped_article(article)
                            
                            show_analysis_animation(console)
                            
                            analysis = critical_analyst.analyze_critically(article, 'it')
                            show_verification_results(analysis, model_name)
                        else:
                            console.print("[red]❌ Impossibile estrarre l'articolo dall'URL fornito[/red]")
                            console.input("\nPremi invio per tornare alla lista")
                            
                    except Exception as e:
                        console.print(f"[red]❌ Errore durante lo scraping/analisi: {e}[/red]")
                        console.input("\nPremi invio per tornare alla lista")
        elif user_input == 'c':
            handle_settings_menu(console)
            settings = load_settings()
            per_page = int(settings.get("articles_per_page", 15))
            total_pages = (len(articles) + per_page - 1) // per_page
        elif user_input == '\r' or user_input == '\n':
            show_article(articles[selected_idx])
            console.input("Premi invio per tornare alla lista: ")
        else:
            try:
                idx = int(user_input)
                if 0 <= idx < len(articles):
                    selected_idx = idx
                    console.print(f"[green]✅ Articolo #{idx} selezionato[/green]")
                    show_article(articles[idx])
                    console.input("Premi invio per tornare alla lista: ")
                else:
                    console.print(f"[red]❌ Articolo #{idx} non esiste. Articoli disponibili: 0-{len(articles)-1}[/red]")
            except ValueError:
                if user_input.strip():
                    console.print(f"[yellow]⚠️ Comando '{user_input}' non riconosciuto. Usa i comandi mostrati sopra.[/yellow]")

if __name__ == "__main__":
    main()
