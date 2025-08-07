
import requests
import json
from abc import ABC, abstractmethod

class AIProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, max_tokens: int = 2048) -> str:
        pass

class OllamaProvider(AIProvider):
    def __init__(self, model: str, url: str):
        self.model = model
        self.url = url
    
    def generate(self, prompt: str, max_tokens: int = 2048) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"num_predict": max_tokens}
        }
        try:
            response = requests.post(self.url, json=payload, timeout=120)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "[Nessuna risposta da Ollama]")
        except Exception as e:
            raise Exception(f"Errore chiamando Ollama: {e}")

class OpenAIProvider(AIProvider):
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.url = "https://api.openai.com/v1/chat/completions"
    
    def generate(self, prompt: str, max_tokens: int = 2048) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens
        }
        try:
            response = requests.post(self.url, json=payload, headers=headers, timeout=60)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            raise Exception(f"Errore chiamando OpenAI: {e}")

class ClaudeProvider(AIProvider):
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.url = "https://api.anthropic.com/v1/messages"
    
    def generate(self, prompt: str, max_tokens: int = 2048) -> str:
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        payload = {
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}]
        }
        try:
            response = requests.post(self.url, json=payload, headers=headers, timeout=60)
            response.raise_for_status()
            data = response.json()
            return data["content"][0]["text"]
        except Exception as e:
            raise Exception(f"Errore chiamando Claude: {e}")

class FallbackAIProvider(AIProvider):
    """Provider con fallback automatico tra diversi servizi AI"""
    
    def __init__(self, providers: list):
        self.providers = providers
    
    def generate(self, prompt: str, max_tokens: int = 2048) -> str:
        for i, provider in enumerate(self.providers):
            try:
                print(f"Tentativo {i+1}/{len(self.providers)} con {provider.__class__.__name__}...")
                result = provider.generate(prompt, max_tokens)
                
                if not result.startswith("[Errore"):
                    print(f"✅ Successo con {provider.__class__.__name__}")
                    return result
                else:
                    print(f"❌ Fallito con {provider.__class__.__name__}: {result}")
                    
            except Exception as e:
                print(f"❌ Errore con {provider.__class__.__name__}: {e}")
                continue
        
        return "[Errore: Tutti i provider AI sono non disponibili. Riprova più tardi.]"

def create_ai_provider(provider: str, settings: dict) -> AIProvider:
    """Factory per creare il provider AI appropriato con fallback automatico"""
    
    if provider == "ollama":
        model = settings.get("model", "qwen2:7b-instruct")
        url = settings.get("ollama_url", "http://localhost:11434/api/generate")
        return OllamaProvider(model, url)
    
    elif provider == "openai":
        api_key = settings.get("openai_api_key")
        model = settings.get("openai_model", "gpt-4")
        if not api_key:
            raise ValueError("OpenAI API key non configurata")
        return OpenAIProvider(api_key, model)
    
    elif provider == "claude":
        api_key = settings.get("claude_api_key")
        model = settings.get("claude_model", "claude-3-5-sonnet-20241022")
        if not api_key:
            raise ValueError("Claude API key non configurata")
        return ClaudeProvider(api_key, model)
    
    else:
        available_providers = []
        
        try:
            url = settings.get("ollama_url", "http://localhost:11434/api/generate")
            model = settings.get("ollama_model", "qwen2:7b-instruct")
            available_providers.append(OllamaProvider(model, url))
        except:
            pass
        
        try:
            api_key = settings.get("openai_api_key")
            if api_key and api_key.strip():
                model = settings.get("openai_model", "gpt-4")
                available_providers.append(OpenAIProvider(api_key, model))
        except:
            pass
        
        try:
            api_key = settings.get("claude_api_key")
            if api_key and api_key.strip():
                model = settings.get("claude_model", "claude-3-5-sonnet-20241022")
                available_providers.append(ClaudeProvider(api_key, model))
        except:
            pass
        
        if not available_providers:
            raise ValueError("Nessun provider AI configurato correttamente")
        
        if len(available_providers) == 1:
            return available_providers[0]
        
        print(f"🔄 Configurato fallback automatico tra {len(available_providers)} provider AI")
        return FallbackAIProvider(available_providers) 