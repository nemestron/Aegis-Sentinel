🛡️ AEGIS SENTINEL

**Autonomous Multi-Agent Financial Intelligence & Sentinel System**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://aegis-sentinel.streamlit.app/)
[![Telegram](https://img.shields.io/badge/Telegram-Channel-blue?logo=telegram)](https://t.me/aegis_sentinel_feed)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-Enabled-red?logo=github-actions)](../../actions)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Live Demo](#live-demo)
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Development Phases](#development-phases)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## 🎯 Overview

**Aegis Sentinel** is a production-grade, autonomous financial intelligence platform that leverages multi-agent AI systems to deliver real-time market analysis, verified insights, and automated reporting. Built with enterprise-grade reliability, the system processes live market data through a sophisticated pipeline of AI agents, each specialized for distinct cognitive tasks.

The system operates 24/7 via GitHub Actions automation, delivering hourly consolidated market briefs while maintaining complete audit trails and source attribution for every insight generated.

---

## 🌐 Live Demo

**Try it now:** [https://aegis-sentinel.streamlit.app/](https://aegis-sentinel.streamlit.app/)

**Join our Telegram Channel:** [https://t.me/aegis_sentinel_feed](https://t.me/aegis_sentinel_feed)

---

## ✨ Key Features

### 🔴 Real-Time Intelligence
- Live market data from yfinance (NSE, BSE, NYSE, NASDAQ)
- Real-time web scraping via DuckDuckGo Search
- Automated hourly briefings via GitHub Actions

### 🧠 Multi-Agent Cognitive System
- **Triage Node**: Filters low-quality information (Llama 3.1 8B)
- **Authentication Node**: Fact-verification against RAG context (Llama 4 Maverick 17B)
- **Synthesis Node**: Generates actionable financial briefs (DeepSeek R1 32B)
- **Formatting Node**: Production-ready output formatting (Llama 3.1 8B)

### 📚 Advanced RAG System
- ChromaDB vector storage with HuggingFace embeddings
- Source link preservation throughout the pipeline
- Semantic similarity search with metadata retention
- No fabricated data—100% source-attributed content

### 🚀 Production Features
- **Autonomous Execution**: Zero human-in-the-loop interruptions
- **Stateful Processing**: SQLite checkpointing for thread isolation
- **Robust Error Handling**: Retry logic with exponential backoff
- **Security**: Secrets management via GitHub Secrets & .env
- **Observability**: Rotating logs with automatic secret redaction

### 📊 Delivery Channels
- **Telegram Bot**: Instant alerts with Markdown formatting
- **Streamlit Dashboard**: Interactive web interface
- **PDF Reports**: Downloadable reports with embedded links
- **GitHub Actions**: Scheduled hourly updates (weekdays)

---

## 🏗️ System Architecture



*Figure 1: Complete system architecture showing data flow from ingestion to delivery*

### Architecture Highlights

1. **Data Sources Layer**: Live APIs (yfinance, DuckDuckGo) with environment-based secrets
2. **Ingestion & Retrieval**: ChromaDB RAG with source link preservation
3. **Cognitive Layer**: LangGraph-based multi-agent system with specialized Groq models
4. **Autonomous Orchestration**: State machine with verification gates and checkpointing
5. **Delivery & Reporting**: Multi-channel distribution with audit trails
6. **User Interfaces**: Streamlit dashboard with manual execution capability
7. **Scheduler & Deployment**: GitHub Actions cron workflows

---

## 🛠️ Tech Stack

### Core Framework
- **LangGraph**: Autonomous state machine orchestration
- **LangChain**: RAG pipeline and agent coordination
- **Groq API**: High-performance LLM inference

### Data & Storage
- **ChromaDB**: Local vector database with embeddings
- **SQLite**: Thread-isolated checkpointing
- **yfinance**: Market data retrieval
- **DuckDuckGo Search**: Web intelligence gathering

### Frontend & Delivery
- **Streamlit**: Interactive web dashboard
- **Telegram Bot API**: Real-time notifications
- **FPDF2**: PDF report generation

### DevOps & Infrastructure
- **GitHub Actions**: CI/CD and scheduled workflows
- **uv (Astral)**: Ultra-fast Python package management
- **Tenacity**: Retry logic with exponential backoff
- **RotatingFileHandler**: Production-grade logging

---

## 📦 Installation

### Prerequisites

- **Python 3.11+**
- **Git**
- **uv** (Astral package manager)
- **Windows 11 PowerShell** (or Linux/macOS terminal)

### Quick Start

```powershell
# Clone the repository
git clone https://github.com/nemestron/Aegis-Sentinel.git
cd Aegis-Sentinel

# Initialize uv environment
uv init
uv venv
.venv\Scripts\activate  # On Linux/macOS: source .venv/bin/activate

# Install dependencies
uv add langgraph langchain langchain-community groq chromadb streamlit \
       python-dotenv yfinance duckduckgo-search fpdf2 tenacity \
       pydantic pytest diskcache pytz

# Create environment file
cp .env.example .env
# Edit .env with your API keys
```

### Environment Configuration

Create a `.env` file at the project root:

```env
# Groq API (Get free key at https://console.groq.com)
GROQ_API_KEY=your_groq_api_key_here

# Telegram Bot (Create via @BotFather)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here
```

---

## 🚀 Usage

### 1. Interactive Dashboard (Recommended)

```bash
uv run streamlit run app.py
```

Access at: `http://localhost:8501`

**Features:**
- Enter ticker symbols (e.g., `RELIANCE.NS`, `AAPL`, `BARC.L`)
- Run real-time analysis with background thread execution
- Download PDF reports with clickable sources
- Manual Telegram delivery option

### 2. Command-Line Execution

```bash
# Single ticker analysis
uv run python -c "from src.graph_engine import invoke_graph_autonomous; invoke_graph_autonomous('TCS.NS')"

# Test memory system
uv run src/test_memory.py

# Test agent personas
uv run src/test_agents.py
```

### 3. Automated Hourly Briefings

The system runs automatically via GitHub Actions:
- **Schedule**: Every weekday at minute 0 (00:00, 01:00, ..., 23:00 UTC)
- **Watchlist**: Pre-configured Indian & US markets
- **Delivery**: Consolidated Telegram message with global headlines

To trigger manually:
1. Go to **Actions** tab in GitHub
2. Select **Hourly Finance Update**
3. Click **Run workflow**

---

## 📁 Project Structure

```
Aegis-Sentinel/
├── .github/workflows/
│   └── hourly-update.yml          # GitHub Actions scheduler
├── src/
│   ├── agents/
│   │   └── nodes.py               # Multi-agent personas (Triage, Auth, Synthesis, Format)
│   ├── delivery/
│   │   └── transmission.py        # Telegram Bot integration
│   ├── memory/
│   │   └── rag_store.py           # ChromaDB RAG implementation
│   ├── reconnaissance/
│   │   ├── market_data.py         # yfinance integration
│   │   └── search.py              # DuckDuckGo web search
│   ├── graph_engine.py            # LangGraph state machine
│   ├── state.py                   # AgentState Pydantic schema
│   └── watchlist.py               # Configured ticker symbols
├── checkpoints/
│   └── aegis.db                   # SQLite checkpoint storage
├── local_db/                      # ChromaDB vector store
├── .env                           # Environment secrets (gitignored)
├── .env.example                   # Template for environment variables
├── .gitignore                     # Git ignore rules
├── app.py                         # Streamlit dashboard
├── scheduled_runner.py            # Hourly briefing generator
├── requirements.txt               # Python dependencies
├── pyproject.toml                 # uv project configuration
└── README.md                      # This file
```

---

## 🔄 Development Phases

| Phase | Version Tag | Focus Area | Status |
|-------|-------------|------------|--------|
| **1** | `v0.1-aegis-command-center` | Environment setup & uv initialization | ✅ Complete |
| **2** | `v0.2-aegis-intel-acquisition` | Data ingestion & RAG vector storage | ✅ Complete |
| **3** | `v0.3-aegis-cognitive-nodes` | LLM personas with Groq models | ✅ Complete |
| **4** | `v0.4-aegis-autonomous-graph` | Autonomous state machine (no HITL) | ✅ Complete |
| **5** | `v0.5-aegis-dissemination` | Telegram delivery & logging | ✅ Complete |
| **6** | `v1.0-aegis-dashboard` | Streamlit UI & PDF generation | ✅ Complete |
| **7** | `v1.1-aegis-scheduler` | Hourly consolidated reporter | ✅ Complete |
| **8** | `v2.0-aegis-sentinel-pro` | GitHub Actions deployment | ✅ Complete |

---

## 📡 API Documentation

### Core Functions

#### `invoke_graph_autonomous(ticker: str) -> dict`

Executes the complete analysis pipeline for a given ticker symbol.

**Parameters:**
- `ticker` (str): Stock symbol (e.g., `"RELIANCE.NS"`, `"AAPL"`)

**Returns:**
```python
{
    "ticker": "RELIANCE.NS",
    "current_price": "₹2,847.50",
    "change_percent": "+1.23%",
    "company_name": "Reliance Industries Limited",
    "final_brief": "Concise 2-3 line financial summary...",
    "source_links": ["https://...", "https://..."],
    "verified": True
}
```

**Example:**
```python
from src.graph_engine import invoke_graph_autonomous

result = invoke_graph_autonomous("TCS.NS")
print(result["final_brief"])
```

#### `send_telegram_message(text: str) -> bool`

Sends formatted message to configured Telegram chat.

**Parameters:**
- `text` (str): Markdown-formatted message (max 4096 chars)

**Returns:**
- `True` on success, `False` on failure

---

## 🔐 Security & Compliance

### Data Integrity Guarantee
✅ **No Fabricated Data**: Every piece of information is sourced from live APIs at runtime  
✅ **Source Attribution**: All outputs include clickable source links  
✅ **Audit Trail**: Complete logging with rotating files and secret redaction  
✅ **Reproducible Outputs**: Deterministic processing with state checkpointing

### Security Measures
- 🔒 Secrets stored in GitHub Secrets (never in code)
- 🔒 `.env` file gitignored and encrypted at rest
- 🔒 API keys redacted from all logs
- 🔒 HTTPS-only external API communication
- 🔒 Least privilege principle for all components

---

## 🧪 Testing

```bash
# Run all tests
uv run pytest

# Test individual components
uv run src/test_memory.py      # RAG storage & retrieval
uv run src/test_agents.py      # Agent persona outputs
uv run src/test_graph.py       # End-to-end graph execution
uv run scheduled_runner.py     # Hourly briefing generation
```

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add amazing feature'`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add type hints to all functions
- Include docstrings for public methods
- Write tests for new features
- Update documentation as needed

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Contact & Connect

**Developer:** Dhiraj Malwade

- **LinkedIn:** [linkedin.com/in/dhiraj-malwade-6a8385399](https://www.linkedin.com/in/dhiraj-malwade-6a8385399/)
- **Telegram Channel:** [t.me/aegis_sentinel_feed](https://t.me/aegis_sentinel_feed)
- **Live Demo:** [aegis-sentinel.streamlit.app](https://aegis-sentinel.streamlit.app/)
- **GitHub:** [github.com/nemestron/Aegis-Sentinel](https://github.com/nemestron/Aegis-Sentinel)

---

## 🙏 Acknowledgments

- **Groq** for ultra-fast LLM inference
- **LangChain & LangGraph** for agent orchestration
- **Streamlit** for rapid dashboard development
- **Astral (uv)** for blazing-fast package management

---

## 📊 System Metrics

| Metric | Value |
|--------|-------|
| **Average Response Time** | < 15 seconds per ticker |
| **Uptime** | 99.9% (GitHub Actions SLA) |
| **Data Freshness** | Real-time (live API calls) |
| **Supported Exchanges** | NSE, BSE, NYSE, NASDAQ, LSE |
| **Model Context Window** | Up to 128K tokens |

---

<div align="center">

**⚡ Built for enterprise & institutional use • Modular • Auditable • Scalable ⚡**

*All outputs generated from live runtime data with preserved source links*

[⬆ Back to Top](#aegis-sentinel)
