# 🪟 Windows Installation Guide

Complete guide to install and run the Terminal News Agent on Windows, starting from Python installation.

---

## 📋 Prerequisites

### 1. **Python Installation**

#### Option A: Download from python.org (Recommended)
1. Go to [python.org/downloads](https://python.org/downloads)
2. Download the latest Python version (3.8 or higher)
3. **IMPORTANT**: During installation, check ✅ "Add Python to PATH"
4. Verify installation by opening Command Prompt:
   ```cmd
   python --version
   pip --version
   ```

#### Option B: Microsoft Store
1. Open Microsoft Store
2. Search for "Python"
3. Install the latest version
4. Verify installation as above

### 2. **Git Installation**
1. Go to [git-scm.com/download/win](https://git-scm.com/download/win)
2. Download and install Git for Windows
3. Use default settings during installation
4. Verify installation:
   ```cmd
   git --version
   ```

---

## 🚀 Installation Steps

### Step 1: Clone the Repository
```cmd
git clone https://github.com/Pinperepette/news_agent.git
cd news_agent
```

### Step 2: Install Dependencies
```cmd
pip install -e .
```

### Step 3: Configure the Application

#### Quick Setup with Claude (Recommended)
1. Get your Claude API key from [console.anthropic.com](https://console.anthropic.com/)
2. Edit `news_agent/settings.ini`:
   ```ini
   provider = claude
   claude_api_key = sk-ant-your-key-here
   ```

#### Local Setup with Ollama
1. Install [Ollama](https://ollama.ai/) for Windows
2. Open Command Prompt and run:
   ```cmd
   ollama pull qwen2:7b-instruct
   ```
3. Edit `news_agent/settings.ini`:
   ```ini
   provider = ollama
   model = qwen2:7b-instruct
   ```

### Step 4: Run the Application
```cmd
python -m news_agent.main
```

---

## 🔧 Configuration Options

### AI Providers

#### Claude (Recommended for best results)
```ini
provider = claude
claude_api_key = your-claude-api-key
claude_model = claude-3-5-sonnet-20241022
```

#### OpenAI
```ini
provider = openai
openai_api_key = your-openai-api-key
openai_model = gpt-4
```

#### Ollama (Local, no internet required)
```ini
provider = ollama
model = qwen2:7b-instruct
```

### News Verification (Optional)
To enable news verification features:
```ini
serpapi_key = your-serpapi-key
```

---

## 🎮 How to Use

### Navigation
- **Arrow Keys**: Navigate between articles
- **Enter**: Open selected article details
- **n**: Next page
- **p**: Previous page
- **o**: Open article in browser
- **s**: Global summary
- **a**: LLM agents menu
- **f**: Next set of articles
- **c**: Configuration menu
- **v**: News verification (if SerpAPI configured)
- **q**: Quit

### LLM Agents
- **Summary**: Generate article summaries
- **Implications**: Analyze consequences
- **Theory**: Build scenarios and connections
- **Universal Analysis**: Multi-thematic framework

### News Verification
- **Standard**: Basic fact-checking
- **Advanced**: Step-by-step reasoning
- **Multi-Agent**: Specialized AI collaboration
- **Custom Text**: Verify any text you input

---

## 🛠️ Troubleshooting

### Common Issues

#### "python is not recognized"
- Python not added to PATH during installation
- **Solution**: Reinstall Python and check "Add Python to PATH"

#### "pip is not recognized"
- pip not installed or not in PATH
- **Solution**: 
  ```cmd
  python -m ensurepip --upgrade
  ```

#### Arrow keys not working
- Windows Terminal or Command Prompt issue
- **Solution**: Use Windows Terminal (available from Microsoft Store)

#### "Module not found" errors
- Dependencies not installed
- **Solution**: 
  ```cmd
  pip install -e . --force-reinstall
  ```

#### Ollama connection issues
- Ollama not running
- **Solution**: 
  ```cmd
  ollama serve
  ```

### Performance Tips

#### For Ollama (Local AI)
- Use smaller models for faster responses
- Close other applications to free up RAM
- Consider using GPU acceleration if available

#### For Cloud AI (Claude/OpenAI)
- Ensure stable internet connection
- API keys have usage limits, monitor your usage

---

## 📁 File Structure
```
news_agent/
├── news_agent/
│   ├── main.py          # Main application
│   ├── ui.py            # User interface
│   ├── agents.py        # AI agents
│   ├── verifier.py      # News verification
│   ├── ai_providers.py  # AI provider management
│   ├── multi_agents.py  # Multi-agent system
│   ├── settings.ini     # Configuration
│   └── settings.py      # Settings management
├── setup.py             # Installation script
├── README.md            # Main documentation
└── WINDOWS_INSTALL.md   # This file
```

---

## 🔗 Useful Links

- **Python**: [python.org](https://python.org)
- **Git**: [git-scm.com](https://git-scm.com)
- **Claude API**: [console.anthropic.com](https://console.anthropic.com)
- **OpenAI API**: [platform.openai.com](https://platform.openai.com)
- **Ollama**: [ollama.ai](https://ollama.ai)
- **SerpAPI**: [serpapi.com](https://serpapi.com)
- **Windows Terminal**: [Microsoft Store](https://apps.microsoft.com/detail/9n0dx20hk701)

---

## 🆘 Need Help?

If you encounter issues:
1. Check this troubleshooting section
2. Verify all prerequisites are installed
3. Ensure you're using the correct commands for Windows
4. Check that your API keys are valid and have sufficient credits

The application is designed to work seamlessly on Windows with full arrow key navigation support! 🎯 