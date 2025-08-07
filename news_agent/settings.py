
import configparser
from pathlib import Path

def load_settings(config_file=None):
    if config_file is None:
        possible_paths = [
            Path.cwd() / "settings.ini",  # Percorso dalla directory corrente (root)
            Path(__file__).parent / "settings.ini",  # Percorso relativo al modulo
            Path.cwd() / "news_agent" / "settings.ini",  # Percorso dalla directory corrente
            Path.home() / ".news_agent" / "settings.ini",  # Percorso home
        ]
        
        for path in possible_paths:
            if path.exists():
                cp = configparser.ConfigParser()
                cp.read(path)
                if 'DEFAULT' in cp and cp['DEFAULT'].get('serpapi_key', '').strip():
                    config_file = path
                    break
        
        if config_file is None:
            for path in possible_paths:
                if path.exists():
                    config_file = path
                    break
    
    cp = configparser.ConfigParser()
    cp.read(config_file)
    
    settings = {}
    
    if 'DEFAULT' in cp:
        settings.update(cp['DEFAULT'])
    
    if 'AI' in cp:
        settings.update(cp['AI'])
    
    if 'News' in cp:
        settings.update(cp['News'])
    
    if 'Sources' in cp:
        settings.update(cp['Sources'])
    
    return settings
