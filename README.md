# Terminal News Agent

**Terminal News Agent** is the ultimate tool for reading, analyzing, and "dissecting" Google News headlines directly from your terminal.  
Not only can you browse the latest news, but you can launch **multiple AI agents** to generate summaries, analyze implications, and build complex scenarios—all with support for local (Ollama) and cloud (OpenAI, Claude) AI providers.

---

## 🚀 Features

- **Real news from Google News** in real-time (via RSS, no sketchy scraping)
- **Interactive terminal table** with keyboard navigation, Rich styling, and focus highlight
- **Multiple AI Providers**: Support for Ollama (local), OpenAI, and Claude
- **Chained LLM agents:**
  - *Summary Agent*: concise, factual abstract
  - *Implications Agent*: in-depth analysis of consequences
  - *Theory Agent*: connects dots and builds scenarios
  - *Universal Analysis Agent*: multi-thematic framework for complex topics
  - *(All agents can be triggered from the terminal UI!)*
- **🔍 Advanced News Verification System** (with SerpAPI):
  - Verify selected articles or custom text
  - **Three verification modes**: Fast, Medium, Comprehensive
  - **Standard and Advanced verification** with step-by-step reasoning
  - Fact-checking search results with full content scraping
  - **Bilingual search** (Italian + English sources)
  - Reliable sources cross-reference
  - AI-powered truth analysis with critical skepticism
  - **Direct truth validation** with clear verdicts (VERA/FALSA/DUBBIA)
- **⚙️ Built-in Settings Manager**: Modify all configuration directly from UI
- **Full article content scraping** for comprehensive analysis
- **Open article in browser** with one key
- **Multi-language** and Google News topic filtering (configurable in settings)
- **No cloud required:**
  - 100% local processing with Ollama, no external APIs needed
  - Cloud options available for higher quality analysis
- **Designed for hacking/extending:** config/code separation, easy to customize
- **Works on Linux, macOS, WSL, Windows Terminal**

---

![Terminal Demo 1](./image/term_1.png)
![Terminal Demo 1](./image/term_2.png)

---

## ⚡ Installation

Clone the repo and install locally:

```bash
git clone https://github.com/Pinperepette/news_agent.git
cd news_agent
pip install .

news-agent
```

## 🔧 Configuration

### Quick Setup

#### 🚀 Fast Start with Claude (Recommended)
1. Get your Claude API key from [console.anthropic.com](https://console.anthropic.com/)
2. Edit `news_agent/settings.ini`:
   ```ini
   provider = claude
   claude_api_key = sk-ant-your-key-here
   ```
3. Run: `python -m news_agent.main`

#### 🏠 Local Setup with Ollama
1. Install [Ollama](https://ollama.ai/)
2. Run: `ollama pull qwen2:7b-instruct`
3. Edit `news_agent/settings.ini`:
   ```ini
   provider = ollama
   model = qwen2:7b-instruct
   ```
4. Run: `python -m news_agent.main`

### ⚙️ Built-in Settings Manager

**NEW**: You can now modify all settings directly from the UI!

1. **Press `c`** in the main menu to open the configuration panel
2. **Select what to modify**:
   - Provider AI (ollama/openai/claude)
   - AI models for each provider
   - API keys (OpenAI, Claude, SerpAPI)
   - General settings (language, RSS feed, articles per page)
   - View current configuration

**No more manual file editing required!** 🎉

### Detailed Configuration

Edit `news_agent/settings.ini`:

```ini
[DEFAULT]
lang = it
topic = https://www.ansa.it/sito/ansait_rss.xml
articles_per_page = 15
provider = ollama
model = qwen2:7b-instruct
ollama_url = http://localhost:11434/api/generate
serpapi_key = 
openai_api_key = 
claude_api_key = 
openai_model = gpt-4
claude_model = claude-3-5-sonnet-20241022
```

### 🤖 AI Provider System

The system uses a **factory pattern** that allows you to easily switch between different AI providers by changing just one line in the configuration.

#### How to Choose Your AI Provider

Simply change the `provider =` line in `settings.ini`:

```ini
# For Ollama (local, free)
provider = ollama

# For OpenAI (cloud, paid)
provider = openai

# For Claude (cloud, paid)
provider = claude
```

#### 1. Claude (Recommended - High Quality)
```ini
provider = claude
claude_api_key = sk-ant-your-claude-key-here
claude_model = claude-3-5-sonnet-20241022
```

**Available Claude Models:**
- `claude-3-opus-20240229` - Most powerful (expensive)
- `claude-3-5-sonnet-20241022` - Balanced (recommended)
- `claude-3-5-sonnet-20240926` - Alternative Sonnet
- `claude-3-5-haiku-20241022` - Fastest (cheapest)

- **Pros**: Excellent reasoning, high quality responses, best for complex analysis
- **Cons**: Requires API key, costs money (~$0.003/1K tokens)
- **Setup**: Get API key from [Anthropic Console](https://console.anthropic.com/)

#### 2. Ollama (Local - Free)
```ini
provider = ollama
model = qwen2:7b-instruct
ollama_url = http://localhost:11434/api/generate
```

**Recommended Models:**
- `qwen2:7b-instruct` - Good balance of speed and quality
- `llama3.2:3b` - Fast and lightweight
- `mistral:7b` - High quality for size
- `codellama:7b` - Good for technical topics

- **Pros**: Free, private, no internet required, no API limits
- **Cons**: Requires local setup, slower than cloud options
- **Setup**: Install Ollama and run `ollama pull qwen2:7b-instruct`

#### 3. OpenAI
```ini
provider = openai
openai_api_key = sk-your-openai-key-here
openai_model = gpt-4
```

**Available Models:**
- `gpt-4` - Most powerful (expensive)
- `gpt-3.5-turbo` - Good balance (cheaper)
- `gpt-4-turbo` - Latest GPT-4 version

- **Pros**: High quality, reliable, excellent for creative tasks
- **Cons**: Requires API key, costs money
- **Setup**: Get API key from [OpenAI Platform](https://platform.openai.com/)

### AI Provider Comparison

| Provider | Cost | Privacy | Quality | Speed | Setup |
|----------|------|---------|---------|-------|-------|
| **Claude** | Pay-per-use | Cloud | Excellent | Fast | API key |
| **Ollama** | Free | 100% Private | Good | Medium | Local install |
| **OpenAI** | Pay-per-use | Cloud | Excellent | Fast | API key |

### How the AI System Works

1. **Configuration Reading**: The program reads `provider =` from `settings.ini`
2. **Provider Creation**: Creates the appropriate AI provider using `create_ai_provider()`
3. **Fallback System**: If multiple providers are configured, automatically tries alternatives if one fails
4. **Unified Interface**: All agents use the same provider for:
   - 📰 Article summarization (`s`)
   - 🤖 LLM agents (`a`)
   - 🔍 News verification (`v`)
5. **Model Name Display**: Shows which model is being used in response titles

### 🔄 Automatic Fallback System

If you have multiple AI providers configured, the system will:
1. **Try the primary provider** first
2. **Automatically switch** to the next available provider if one fails
3. **Show feedback** about which provider is being used
4. **Ensure continuity** even with temporary server errors

**Example**: If Claude returns a 529 error, the system automatically switches to OpenAI or Ollama.

### News Verification Setup

To enable the news verification feature:

1. Get a free API key from [SerpAPI](https://serpapi.com/)
2. Add your key to `settings.ini`:
   ```ini
   serpapi_key = your_serpapi_key_here
   ```
3. The verification option (`v`) will appear in the menu

**Verification Features:**
- **Three search modes**: Fast (quick), Medium (balanced), Comprehensive (thorough)
- Searches for fact-checking information in both Italian and English
- Cross-references with reliable sources
- **Scrapes full content** of verification articles
- Uses AI to analyze truthfulness with critical skepticism
- Provides detailed verification report
- **Advanced verification** with step-by-step reasoning (Chain-of-Thought)

---

## 🎮 Usage

### Navigation
- **↑↓** Arrow keys: Navigate between articles
- **w/z**: Alternative navigation keys
- **Enter**: Open selected article details
- **f**: Move to next article (auto-advance)
- **n/p**: Next/Previous page
- **Number**: Select specific article by number

### Actions
- **o**: Open article in browser
- **s**: Generate article summary (with full content scraping)
- **a**: Run LLM agents on selected article
- **v**: Verify news (if SerpAPI configured)
- **c**: **NEW** - Open configuration settings menu
- **q**: Quit

### LLM Agents Menu (a)
1. **Summary**: Quick factual summary using full article content
2. **Implications**: Social, economic, political consequences
3. **Theory/Scenario**: Complex scenarios and connections
4. **Universal Analysis**: Multi-thematic framework for complex topics
5. **All Agents**: Run all agents in sequence

### News Verification (v)
**NEW**: Multi-agent verification system with specialized agents!

#### **📰 SELECTED ARTICLE:**
1. **Standard Verification**: Basic critical analysis of selected article
2. **Standard Truth Validation**: Direct truth validation with confidence level
3. **Multi-Agent System** 🤖: **NEW** - Complete analysis with 6 specialized agents

#### **📝 CUSTOM TEXT:**
4. **Standard Verification**: Basic critical analysis of custom text
5. **Advanced Verification (Step-by-Step)**: Detailed analysis with structured reasoning
6. **Advanced Truth Validation**: Advanced truth validation with complex analysis

#### **🤖 Multi-Agent System (Option 3):**
The most comprehensive verification system using 6 specialized agents:

- **🔍 Investigator Agent**: Finds and collects key information
- **📊 Methodological Analyst Agent**: Evaluates scientific studies
- **🎯 Verifier Agent**: Checks specific facts
- **⚖️ Judge Agent**: Analyzes bias and conflicts of interest
- **🌐 Consensus Agent**: Analyzes scientific consensus
- **🧠 Synthesizer Agent**: Combines all results for final verdict

#### **⚡ Verification Modes:**
- **Fast** (~30 sec): Quick fact-checking, basic sources, Italian only
- **Medium** (~2 min): Balanced approach, bilingual sources, full scraping
- **Comprehensive** (~5 min): Comprehensive analysis, complete bilingual sources

#### **🎯 When to Use Each Type:**

| Type | Use Case | Time | Complexity |
|------|----------|------|------------|
| **Standard** | Quick verification | ~1-2 min | Medium |
| **Multi-Agent** | Complex/controversial news | ~3-5 min | High |
| **Step-by-Step** | Detailed analysis | ~2-3 min | High |
| **Truth Validation** | Direct true/false assessment | ~1-2 min | Medium |

The verification system:
- **Bilingual search** (Italian + English sources)
- Searches for fact-checking information
- Cross-references with reliable sources
- **Scrapes full content** of verification articles
- Uses AI to analyze truthfulness with **critical analysis**
- Provides detailed verification report with content status
- **Advanced agents** use Chain-of-Thought reasoning for complex analysis

### ⚙️ Configuration Menu (c)
**NEW**: Built-in settings manager!

1. **Modify AI Provider**: Switch between ollama/openai/claude
2. **Modify AI Model**: Change AI models for each provider
3. **Modify API Keys**: Add/update API keys
4. **Modify General Settings**: Language, RSS feed, articles per page
5. **View Current Configuration**: See all current settings

---

## 🤖 LLM Agents

The system includes five specialized agents that work with **any AI provider**:

1. **Summary Agent**: Creates concise, factual summaries using full article content
2. **Implications Agent**: Analyzes social, economic, and political consequences
3. **Theory Agent**: Builds complex scenarios and connections
4. **Universal Analysis Agent**: Multi-thematic framework for complex topics
5. **Verification Agent**: Evaluates news truthfulness using multiple sources
6. **Truth Validation Agent**: Provides direct verdict (VERA/FALSA/DUBBIA) with confidence level

### Advanced Verification Agents

**NEW**: Multi-agent verification system with specialized roles!

#### **🤖 Multi-Agent System (Option 3)**
The most comprehensive verification system using 6 specialized agents that work together:

1. **🔍 Investigator Agent**
   - Finds and collects key information from sources
   - Identifies scientific studies mentioned
   - Detects specific claims to verify
   - Identifies potential biased sources

2. **📊 Methodological Analyst Agent**
   - Evaluates methodology of each scientific study
   - Checks journal quality and peer review process
   - Identifies methodological criticisms
   - Analyzes statistical robustness
   - Distinguishes between high-quality studies and predatory journals

3. **🎯 Verifier Agent**
   - Checks veracity of specific claims
   - Looks for contradictions between sources
   - Identifies temporal inconsistencies
   - Detects data manipulations
   - Finds unverifiable statements

4. **⚖️ Judge Agent**
   - Analyzes conflicts of interest
   - Identifies funding sources
   - Detects selection bias, confirmation bias
   - Finds cherry-picking of data
   - Evaluates source reliability

5. **🌐 Consensus Agent**
   - Analyzes scientific consensus on the topic
   - Evaluates quality of consensus
   - Identifies outlier studies and their quality
   - Determines if consensus is strong (90%+) or weak (60-90%)

6. **🧠 Synthesizer Agent**
   - Combines all agent results
   - Weighs evidence based on quality
   - Considers scientific consensus
   - Evaluates conflicts of interest
   - Reaches final verdict

#### **📋 Standard Verification (Options 1, 4)**
- Basic fact-checking and source analysis
- Suitable for most verification needs
- Faster processing (~1-2 minutes)

#### **🧠 Advanced Verification (Options 5, 6)**
- **Chain-of-Thought reasoning**: 6-step structured analysis
- **Critical analysis**: Evaluates each study individually
- **Methodology assessment**: Checks study quality and peer review
- **Consensus analysis**: Verifies scientific agreement
- **Comprehensive investigation**: Deeper analysis of complex topics

**Advanced agents are specifically designed to:**
- Evaluate each scientific study individually (methodology, quality, consensus)
- Check funding sources and conflicts of interest
- Verify if criticisms or replications of specific studies exist
- Distinguish between objective facts and subjective interpretations
- Provide evidence-based analysis of controversial topics

### Universal Analysis Framework

The **Universal Analysis Agent** uses a structured methodology for analyzing complex topics:

- **Factual Analysis**: Identifies verifiable facts and context
- **Multi-dimensional Analysis**: Social, economic, political, technological, environmental dimensions
- **Critical Analysis**: Bias identification, credibility assessment, interest analysis
- **Forward-looking Analysis**: Probable scenarios, strategic implications, open questions
- **Methodological Synthesis**: Confidence levels and recommendations

This framework works on any complex topic and provides systematic, evidence-based analysis.

### Truth Validation Agent

The **Truth Validation Agent** provides a direct and clear assessment of news truthfulness:

- **🎯 Direct Verdict**: [TRUE] / [FALSE] / [DOUBTFUL] / [INSUFFICIENT DATA]
- **📊 Confidence Level**: [HIGH] / [MEDIUM] / [LOW] 
- **🔍 Red Flags**: Identifies bias, suspicious sources, contradictions
- **✅ Confirmations**: Lists sources that support or contradict the news
- **📝 Clear Reasoning**: Explains the verdict with evidence

This agent is specifically designed to give users a clear, actionable assessment of whether a news item is true or false.

### Content Processing

**All agents now use full article content:**
- Articles are automatically scraped for complete text
- Fallback to RSS summary if scraping fails
- Google News links are properly resolved
- Content is cleaned and optimized for AI analysis

---

## 🔧 Advanced Configuration

### RSS Feed Configuration

You can use direct RSS feeds instead of Google News:

```ini
# Direct RSS feed (recommended for better scraping)
topic = https://www.ansa.it/sito/ansait_rss.xml

# Or Google News topic ID
topic = CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtbDBHZ0pKVkNnQVAB
```

### Language and Region

```ini
lang = it          # Language code (it, en, es, fr, de, etc.)
articles_per_page = 15  # Number of articles per page
```

### Model-Specific Settings

Each provider supports different models. Experiment to find the best for your use case:

```ini
# Ollama models
model = qwen2:7b-instruct
model = llama3.2:3b
model = mistral:7b

# OpenAI models
openai_model = gpt-4
openai_model = gpt-3.5-turbo

# Claude models
claude_model = claude-3-5-sonnet-20241022
claude_model = claude-3-5-haiku-20241022
```

---

## 🚀 Getting Started Examples

### Example 1: Quick Start with Claude
```ini
provider = claude
claude_api_key = sk-ant-your-key-here
claude_model = claude-3-5-sonnet-20241022
```

### Example 2: Local Setup with Ollama
```ini
provider = ollama
model = qwen2:7b-instruct
```

### Example 3: OpenAI Setup
```ini
provider = openai
openai_api_key = sk-your-key-here
openai_model = gpt-4
```

### Example 4: Full Configuration with Verification
```ini
provider = claude
claude_api_key = sk-ant-your-key-here
claude_model = claude-3-5-sonnet-20241022
serpapi_key = your_serpapi_key_here
topic = https://www.ansa.it/sito/ansait_rss.xml
```

All agents work with any provider - choose based on your needs for privacy, cost, and quality!

---

## 🔄 Recent Updates

### Latest Features Added:
- **⚙️ Built-in Settings Manager**: Modify all configuration from UI (press `c`)
- **🤖 Multi-Agent Verification System**: 6 specialized agents working together
- **🔍 Advanced Verification Modes**: Fast/Medium/Comprehensive search modes
- **🧠 Chain-of-Thought Reasoning**: Step-by-step analysis for complex verification
- **🌍 Bilingual Search**: Italian + English sources for comprehensive fact-checking
- **📊 Critical Analysis**: Individual evaluation of scientific studies
- **📈 Consensus Analysis**: Scientific consensus verification
- **🎯 Specialized Agent Roles**: Investigator, Methodologist, Verifier, Judge, Consensus, Synthesizer

### Verification Improvements:
- **Multi-agent system** with 6 specialized agents for comprehensive analysis
- **Three search modes** for different needs and time constraints
- **Advanced agents** with structured reasoning for complex topics
- **Critical analysis** that evaluates each study individually
- **Consensus analysis** to verify scientific agreement
- **Bilingual search capabilities** for comprehensive fact-checking
- **Specialized agent workflow** for systematic verification

