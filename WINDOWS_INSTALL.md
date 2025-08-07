# 🪟 Windows Installation Guide

**Complete setup guide for News Agent Pro on Windows**

## 📋 **Prerequisites**

### **System Requirements**
- Windows 10/11 (64-bit)
- Python 3.8 or higher
- 4GB RAM minimum (8GB recommended)
- 2GB free disk space

### **Required Software**
- [Python 3.8+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/download/win) (optional, for cloning)
- [Windows Terminal](https://apps.microsoft.com/detail/9n0dx20hk701) (recommended)

## 🚀 **Installation Steps**

### **Step 1: Install Python**

1. **Download Python**:
   - Go to [python.org](https://www.python.org/downloads/)
   - Download Python 3.8 or higher
   - **IMPORTANT**: Check "Add Python to PATH" during installation

2. **Verify Installation**:
   ```cmd
   python --version
   pip --version
   ```

### **Step 2: Clone/Download Repository**

**Option A: Using Git (Recommended)**
```cmd
git clone https://github.com/your-repo/news_agent.git
cd news_agent
```

**Option B: Manual Download**
- Download ZIP from GitHub
- Extract to desired folder
- Open Command Prompt in the folder

### **Step 3: Install Dependencies**

```cmd
# Install the package in development mode
pip install -e .

# Or install requirements directly
pip install -r requirements.txt
```

### **Step 4: Configure API Keys**

1. **Copy configuration template**:
   ```cmd
   copy settings.ini.example settings.ini
   ```

2. **Edit settings.ini** with your API keys (see detailed setup below)

## 🔑 **Detailed API Setup Guide**

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
1. **Install Ollama**: Download from [ollama.ai](https://ollama.ai)
2. **Start Ollama**: Open Command Prompt and run `ollama serve`
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

## 🎮 **How to Use**

### **Launch the Application**

```cmd
# From the project directory
python -m news_agent.main
```

### **Navigation Controls**

#### **Main Menu**
- **Arrow Keys**: Navigate between options
- **Enter**: Select option
- **q**: Quit application

#### **Article List**
- **↑↓**: Navigate between articles
- **Enter**: Open selected article
- **n**: Next page
- **p**: Previous page
- **o**: Open article in browser
- **v**: Critical analysis
- **c**: Configuration
- **q**: Quit

#### **Analysis Mode**
- **1**: Analyze selected article
- **2**: Custom text analysis
- **3**: URL analysis
- **0**: Back to main menu

## 🤖 **AI Agents Overview**

### **🔬 Scientific Agent**
- **Purpose**: Evaluates research methodology and scientific studies
- **Focus**: 
  - Access to original data vs. reconstructions
  - Experimental protocol rigor
  - Instrumentation quality
  - Peer review status
  - Replicability of methods

### **🏛️ Political Agent**
- **Purpose**: Analyzes political statements and government sources
- **Focus**:
  - Official declarations
  - Government communications
  - Political party statements
  - Institutional sources

### **💻 Technology Agent**
- **Purpose**: Verifies tech announcements and innovations
- **Focus**:
  - Official company announcements
  - Patent information
  - Technical documentation
  - Industry expert opinions

### **💰 Economic Agent**
- **Purpose**: Checks financial data and economic reports
- **Focus**:
  - Official financial reports
  - Economic indicators
  - Market data
  - Expert economic analysis

### **🌍 Universal Agent**
- **Purpose**: General fact-checking and cross-verification
- **Focus**:
  - Multiple source verification
  - Cross-reference checking
  - General credibility assessment

## 🌍 **Supported Languages**

### **News Sources**
- 🇮🇹 **Italian**: ANSA, Repubblica, Corriere della Sera
- 🇺🇸 **English**: Reuters, BBC, CNN, TechCrunch
- 🇫🇷 **French**: Le Monde, Le Figaro, Les Echos
- 🇪🇸 **Spanish**: El País, El Mundo, ABC
- 🇩🇪 **German**: Der Spiegel, Die Zeit, Süddeutsche

### **Output Languages**
- 🇮🇹 Italian
- 🇺🇸 English
- 🇫🇷 French
- 🇩🇪 German
- 🇪🇸 Spanish
- 🇵🇹 Portuguese
- 🇳🇱 Dutch
- 🇷🇺 Russian
- 🇨🇳 Chinese
- 🇯🇵 Japanese
- 🇰🇷 Korean

## ⚙️ **Configuration**

### **AI Provider Settings**

#### **OpenAI Configuration**
```ini
[AI]
provider = openai
openai_api_key = your-openai-api-key
openai_model = gpt-4
```

#### **Claude Configuration**
```ini
[AI]
provider = claude
claude_api_key = your-claude-api-key
claude_model = claude-3-sonnet-20240229
```

#### **Ollama Configuration (Local)**
```ini
[AI]
provider = ollama
model = qwen2:7b-instruct
```

### **News Verification (Optional)**
```ini
[News]
serpapi_key = your-serpapi-key
scrapingdog_api_key = your-scrapingdog-key
```

### **General Settings**
```ini
[General]
default_language = en
articles_per_page = 15
search_timeout = 30
enable_analytics = true
```

## 🛠️ **Troubleshooting**

### **Common Issues**

#### **"python is not recognized"**
- Python not added to PATH during installation
- **Solution**: Reinstall Python and check "Add Python to PATH"

#### **"pip is not recognized"**
- pip not installed or not in PATH
- **Solution**: 
  ```cmd
  python -m ensurepip --upgrade
  ```

#### **Arrow keys not working**
- Windows Terminal or Command Prompt issue
- **Solution**: Use Windows Terminal (available from Microsoft Store)

#### **"Module not found" errors**
- Dependencies not installed
- **Solution**: 
  ```cmd
  pip install -e . --force-reinstall
  ```

#### **Ollama connection issues**
- Ollama not running
- **Solution**: 
  ```cmd
  ollama serve
  ```

### **Performance Tips**

#### **For Ollama (Local AI)**
- Use smaller models for faster responses
- Close other applications to free up RAM
- Consider using GPU acceleration if available

#### **For Cloud AI (Claude/OpenAI)**
- Ensure stable internet connection
- Use appropriate model sizes for your needs
- Monitor API usage and costs

### **Getting Help**

1. **Check the main README**: [README.md](README.md)
2. **Review configuration examples**
3. **Check test files for usage examples**
4. **Verify API keys are correct**
5. **Ensure all dependencies are installed**

## 🔧 **Advanced Configuration**

### **Custom Model Settings**

#### **Ollama Models**
```ini
[AI]
provider = ollama
model = llama2:7b
# Available models: llama2:7b, llama2:13b, qwen2:7b, mistral:7b
```

#### **OpenAI Models**
```ini
[AI]
provider = openai
openai_model = gpt-4-turbo
# Available models: gpt-4, gpt-4-turbo, gpt-3.5-turbo
```

### **Analytics Configuration**
```ini
[Analytics]
enable_tracking = true
db_path = news_analytics.db
export_format = json
```

### **Search Configuration**
```ini
[Search]
timeout = 30
max_results = 10
cache_enabled = true
cache_duration = 3600
```

## 📊 **Features Overview**

### **Core Features**
- ✅ **Multi-Agent Analysis**: Specialized AI agents for different domains
- ✅ **Intelligent Routing**: Automatic agent selection based on content
- ✅ **Multilingual Support**: Multiple languages for sources and output
- ✅ **Rich Interface**: Beautiful terminal-based UI
- ✅ **Analytics Tracking**: Complete session and performance monitoring
- ✅ **Flexible Configuration**: Easy customization of all settings

### **Analysis Capabilities**
- 🔬 **Scientific Evaluation**: Research methodology assessment
- 🏛️ **Political Analysis**: Government and policy verification
- 💻 **Technology Verification**: Tech announcement validation
- 💰 **Economic Fact-Checking**: Financial data verification
- 🌍 **Universal Fact-Checking**: General news verification

### **User Experience**
- 🎨 **Modern UI**: Rich colors and intuitive navigation
- ⌨️ **Keyboard Controls**: Full keyboard navigation
- 📊 **Real-time Stats**: Live performance monitoring
- 🔄 **Progress Indicators**: Visual feedback for operations
- 📤 **Data Export**: Multiple export formats

---

**News Agent Pro** - Advanced AI-powered news analysis and fact-checking system for Windows

For the complete documentation, see [README.md](README.md) 