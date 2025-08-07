# �� News Agent Pro

**Advanced AI-Powered News Analysis & Fact-Checking System**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Rich](https://img.shields.io/badge/Rich-UI-brightgreen.svg)](https://rich.readthedocs.io)
[![AI](https://img.shields.io/badge/AI-Powered-magenta.svg)](https://openai.com)

## 🚀 **Key Features**

### 🧠 **Intelligent Critical Analysis**
- **🔬 Scientific Agent**: Evaluates research methodology and scientific rigor
- **🏛️ Political Agent**: Analyzes political statements and government sources
- **💻 Technology Agent**: Verifies tech announcements and innovations
- **💰 Economic Agent**: Checks financial data and economic reports
- **🌍 Universal Agent**: General fact-checking and cross-verification

### 🎯 **Multi-Agent Orchestration**
- **Intelligent Routing**: AI automatically selects the most appropriate agents
- **Collaborative Verification**: Multiple agents work together for comprehensive analysis
- **Domain Detection**: Automatic classification of news by topic
- **Specialized Evaluation**: Each agent uses domain-specific criteria

### 🌍 **Multilingual Support**
- **Flexible Sources**: Select news sources from any language
- **Customizable Output**: Receive results in your preferred language
- **Automatic Language Detection**: Smart language recognition
- **Intelligent Translation**: Seamless cross-language analysis

### 📊 **Advanced Analytics & Tracking**
- **SQLite Database**: Complete session and performance tracking
- **Detailed Statistics**: Per-session and global analytics
- **Customizable Reports**: Data export and analysis
- **Real-time Monitoring**: Performance tracking

### 🎨 **Modern Rich Interface**
- **Beautiful UI**: Rich colors and animations
- **Interactive Dashboard**: Real-time statistics
- **Progress Indicators**: Visual feedback for long operations
- **Keyboard Navigation**: Intuitive shortcuts and controls

## 📦 **Installation**

### Requirements
- Python 3.8+
- Ollama (for local models) or OpenAI/Claude API keys

### Quick Setup
```bash
# Clone the repository
git clone <repository-url>
cd news_agent

# Install dependencies
pip install -e .

# Configure API keys
cp settings.ini.example settings.ini
# Edit settings.ini with your API keys

# Start the application
python -m news_agent.main
```

### Windows Installation
For detailed Windows installation instructions, see [WINDOWS_INSTALL.md](WINDOWS_INSTALL.md)

## 🔑 **API Keys Setup**

### **🤖 AI Providers**

#### **OpenAI (Paid - Cloud)**
1. **Get API Key**: Go to [platform.openai.com](https://platform.openai.com)
2. **Sign up/Login**: Create account or login
3. **Add Payment Method**: Credit card required
4. **Get API Key**: Go to "API Keys" → "Create new secret key"
5. **Configure**:
   ```ini
   [AI]
   provider = openai
   openai_api_key = sk-your-key-here
   openai_model = gpt-4
   ```

#### **Claude (Paid - Cloud)**
1. **Get API Key**: Go to [console.anthropic.com](https://console.anthropic.com)
2. **Sign up/Login**: Create account or login
3. **Add Payment Method**: Credit card required
4. **Get API Key**: Go to "API Keys" → "Create key"
5. **Configure**:
   ```ini
   [AI]
   provider = claude
   claude_api_key = sk-ant-your-key-here
   claude_model = claude-3-sonnet-20240229
   ```

#### **Ollama (Free - Local)**
1. **Install Ollama**: 
   - **macOS/Linux**: `curl -fsSL https://ollama.ai/install.sh | sh`
   - **Windows**: Download from [ollama.ai](https://ollama.ai)
2. **Start Ollama**: `ollama serve`
3. **Download Model**: `ollama pull qwen2:7b-instruct`
4. **Configure**:
   ```ini
   [AI]
   provider = ollama
   model = qwen2:7b-instruct
   ```

### **🔍 News Verification APIs (Optional)**

#### **SerpAPI (Paid - Web Search)**
1. **Get API Key**: Go to [serpapi.com](https://serpapi.com)
2. **Sign up**: Create account
3. **Add Payment Method**: Credit card required
4. **Get API Key**: Dashboard → "API Key"
5. **Configure**:
   ```ini
   [News]
   serpapi_key = your-serpapi-key
   ```

#### **ScrapingDog (Paid - Content Extraction)**
1. **Get API Key**: Go to [scrapingdog.com](https://scrapingdog.com)
2. **Sign up**: Create account
3. **Add Payment Method**: Credit card required
4. **Get API Key**: Dashboard → "API Key"
5. **Configure**:
   ```ini
   [News]
   scrapingdog_api_key = your-scrapingdog-key
   ```

### **💰 Pricing Information**

#### **OpenAI**
- **GPT-4**: ~$0.03 per 1K tokens
- **GPT-3.5**: ~$0.002 per 1K tokens
- **Free Tier**: $5 credit for new users

#### **Claude**
- **Claude 3 Sonnet**: ~$0.015 per 1K tokens
- **Claude 3 Haiku**: ~$0.0025 per 1K tokens
- **Free Tier**: $5 credit for new users

#### **SerpAPI**
- **Starter**: $50/month for 5,000 searches
- **Basic**: $100/month for 12,500 searches
- **Pro**: $250/month for 35,000 searches

#### **ScrapingDog**
- **Starter**: $29/month for 1,000 requests
- **Basic**: $99/month for 5,000 requests
- **Pro**: $299/month for 20,000 requests

#### **Ollama**
- **Free**: No cost, runs locally
- **Hardware**: Requires 8GB+ RAM for good performance

### **⚙️ Complete Configuration Example**

```ini
[AI]
provider = openai
openai_api_key = sk-your-openai-key-here
openai_model = gpt-4

[News]
serpapi_key = your-serpapi-key
scrapingdog_api_key = your-scrapingdog-key

[General]
default_language = en
articles_per_page = 15
search_timeout = 30
enable_analytics = true
```

## 🎯 **How to Use**

### 🚀 **Quick Mode**
1. Launch the application
2. Select "Quick Mode"
3. System automatically analyzes predefined sources
4. Receive results in your preferred language

### 🔍 **Custom Analysis**
1. **Select Sources**: Choose from multiple languages
2. **Choose Output Language**: Independent of source language
3. **Critical Analysis**: AI analyzes like an expert
4. **Detailed Results**: Plausibility assessment and suspicious points

### 📝 **Manual Analysis**
1. Enter article title and content
2. System automatically detects language
3. Receive complete critical analysis
4. Strategic queries for verification

## 🤖 **AI Agents Overview**

### 🔬 **Scientific Agent**
- **Purpose**: Evaluates research methodology and scientific studies
- **Focus**: 
  - Access to original data vs. reconstructions
  - Experimental protocol rigor
  - Instrumentation quality
  - Peer review status
  - Replicability of methods
- **Icon**: 🔬

### 🏛️ **Political Agent**
- **Purpose**: Analyzes political statements and government sources
- **Focus**:
  - Official declarations
  - Government communications
  - Political party statements
  - Institutional sources
- **Icon**: 🏛️

### 💻 **Technology Agent**
- **Purpose**: Verifies tech announcements and innovations
- **Focus**:
  - Official company announcements
  - Patent information
  - Technical documentation
  - Industry expert opinions
- **Icon**: 💻

### 💰 **Economic Agent**
- **Purpose**: Checks financial data and economic reports
- **Focus**:
  - Official financial reports
  - Economic indicators
  - Market data
  - Expert economic analysis
- **Icon**: 💰

### 🌍 **Universal Agent**
- **Purpose**: General fact-checking and cross-verification
- **Focus**:
  - Multiple source verification
  - Cross-reference checking
  - General credibility assessment
- **Icon**: 🌍

## 🌍 **Supported Sources**

### 🇮🇹 **Italian**
- ANSA
- Repubblica
- Corriere della Sera
- Il Sole 24 Ore
- La Stampa

### 🇺🇸 **English**
- Reuters
- BBC News
- CNN
- TechCrunch
- Wired
- The Verge

### 🇫🇷 **French**
- Le Monde
- Le Figaro
- Les Echos
- L'Express

### 🇪🇸 **Spanish**
- El País
- El Mundo
- ABC
- La Vanguardia

### 🇩🇪 **German**
- Der Spiegel
- Die Zeit
- Süddeutsche Zeitung
- Frankfurter Allgemeine

## 🎮 **Navigation & Controls**

### **Main Menu**
- **Arrow Keys**: Navigate between options
- **Enter**: Select option
- **q**: Quit application

### **Article List**
- **↑↓**: Navigate articles
- **Enter**: Open selected article
- **n**: Next page
- **p**: Previous page
- **o**: Open article in browser
- **v**: Critical analysis
- **c**: Configuration
- **q**: Quit

### **Analysis Mode**
- **1**: Analyze selected article
- **2**: Custom text analysis
- **3**: URL analysis
- **0**: Back to main menu

## ⚙️ **Configuration**

### **AI Provider Settings**
- **Ollama** (Local - no internet required)
- **OpenAI** (GPT-4/GPT-3.5)
- **Claude** (Anthropic)
- **Auto** (Automatic fallback)

### **API Keys**
- OpenAI API Key
- Claude API Key
- SerpAPI Key (for web search)
- ScrapingDog API Key (for content extraction)

### **General Settings**
- Default language
- Number of results per page
- Search timeout
- Cache settings

## 🔧 **Technical Architecture**

### **Core Components**
- **Critical Analyst**: Main analysis engine
- **Intelligent Orchestrator**: Agent selection and coordination
- **Specialized Agents**: Domain-specific analysis
- **Multilingual System**: Language handling
- **Rich UI**: User interface

### **Data Flow**
1. **Input**: Article or text
2. **Analysis**: Critical assessment
3. **Routing**: Agent selection
4. **Verification**: Multi-source checking
5. **Evaluation**: Final assessment
6. **Output**: Detailed report

## 📊 **Analytics & Reports**

### **Session Tracking**
- Articles analyzed
- Sources used
- Analysis time
- Agent performance

### **Global Statistics**
- Total articles processed
- Success rate
- Most used sources
- Performance trends

### **Export Options**
- CSV reports
- JSON data
- Custom formats

## 🛠️ **Development**

### **Project Structure**
```
news_agent/
├── news_agent/
│   ├── main.py                 # Main application
│   ├── critical_analyst.py     # Critical analysis logic
│   ├── intelligent_orchestrator.py  # Agent coordination
│   ├── specialized_agents.py   # Domain-specific agents
│   ├── multilingual_system.py  # Language handling
│   ├── analytics.py            # Analytics system
│   ├── ui.py                   # User interface
│   └── settings.py             # Configuration
├── tests/                      # Test files
├── requirements.txt
├── settings.ini
└── README.md
```

### **Running Tests**
```bash
# Run all tests
python -m pytest

# Run specific test
python test_critical_analyst.py
python test_integration.py
```

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 **License**

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 **Support**

For issues and questions:
- Check the [WINDOWS_INSTALL.md](WINDOWS_INSTALL.md) for Windows-specific help
- Review the configuration examples
- Check the test files for usage examples

---

**News Agent Pro** - Advanced AI-powered news analysis and fact-checking system
