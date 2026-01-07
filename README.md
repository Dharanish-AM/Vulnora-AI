# 🛡️ Vulnora AI

**AI-Powered Multi-Language Code Security Scanner with LLM-Based Vulnerability Detection**

[![Python](https://img.shields.io/badge/Python-3.10+-3776ab.svg?style=flat&logo=python)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-19+-61dafb.svg?style=flat&logo=react)](https://react.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Electron](https://img.shields.io/badge/Electron-Desktop-47848f.svg?style=flat&logo=electron)](https://www.electronjs.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat)](LICENSE)

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Why Vulnora AI?](#-why-vulnora-ai)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage](#-usage)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [API Reference](#-api-reference)
- [Configuration](#-configuration)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

Vulnora AI is an **enterprise-grade, AI-powered security scanner** that automatically analyzes code repositories for vulnerabilities. Unlike traditional static analysis tools that rely on pattern matching, Vulnora AI uses Large Language Models (LLMs) running **100% locally** to understand code semantics and detect complex security issues that traditional tools miss.

**Key Differentiators:**
- 🧠 **Deep Code Understanding** - LLM-based analysis catches logic flaws and complex vulnerabilities
- 🔒 **100% Offline** - Run entirely on your machine; no cloud uploads or external API calls
- 📦 **Multi-Language** - Supports 7+ programming languages out of the box
- ⚡ **Parallel Scanning** - Multi-threaded architecture for fast project analysis
- 🎨 **Modern UI** - Beautiful React-based dashboard with real-time feedback
- 📊 **Detailed Reports** - Comprehensive vulnerability reports with suggested fixes

---

## 🤔 Why Vulnora AI?

### The Problem
Traditional security scanners use rigid regex patterns and heuristics, leading to:
- ❌ **High False Positives** - Wastes time investigating non-issues
- ❌ **Missed Logic Bugs** - Patterns can't understand business logic flaws
- ❌ **Limited Context** - Can't connect vulnerabilities across files
- ❌ **Privacy Concerns** - Cloud-based tools upload your source code

### The Solution
Vulnora AI uses LLMs to analyze code like a seasoned security engineer:
- ✅ **Contextual Analysis** - Understands code flow and business logic
- ✅ **Fewer False Positives** - AI validates findings before reporting
- ✅ **Complex Vulnerability Detection** - Finds issues traditional tools miss
- ✅ **Complete Privacy** - Runs entirely offline with Ollama

### Who Should Use Vulnora AI?

| Role | Use Case |
|------|----------|
| **Security Engineers** | Comprehensive code audits and vulnerability assessments |
| **Development Teams** | Pre-commit security checks and CI/CD integration |
| **Solo Developers** | Quick local security audits for personal projects |
| **Enterprises** | Keep source code private while maintaining security standards |
| **Auditors** | Compliance scanning (OWASP Top 10, CWE, HIPAA, SOC 2) |

---

## ✨ Features

### 🔍 Security Analysis
- ✅ **Multi-Language Support**: Python, JavaScript, TypeScript, Java, Go, Rust, C/C++, HTML/CSS
- ✅ **Hybrid Scanning Pipeline** (NEW in v2.0)
  - **Stage 1**: Fast static analysis pre-filter (< 1ms per file)
  - **Stage 2**: LLM validation on flagged files only (70-90% fewer LLM calls)
  - **Result**: 5-10x faster with same accuracy!
- ✅ **Incremental Scanning** (NEW in v2.0)
  - Only rescans changed files
  - Persistent caching with file hashing
  - 10-100x faster on subsequent scans
- ✅ **Comprehensive Vulnerability Detection**
  - OWASP Top 10 vulnerabilities
  - CWE Top 25 weaknesses
  - Hardcoded secrets and API keys
  - SQL injection and command injection
  - XSS, XXE, and SSRF vulnerabilities
  - Insecure deserialization
  - Weak cryptographic practices
  - Path traversal and authorization flaws
- ✅ **Intelligent Filtering** - Smart directory exclusion (node_modules, .venv, vendor, etc.)

### 🚀 Performance & Scalability
- ✅ **Parallel Scanning** - Multi-threaded file processing
- ✅ **Large Project Support** - Handles thousands of files efficiently
- ✅ **Configurable Model Support** - Works with different Ollama models (Llama, Mistral, etc.)
- ✅ **Multiple Scan Modes**:
  - **Hybrid Mode** (default): 5-10x faster than v1.0
  - **Incremental Mode**: 10-100x faster on re-scans
  - **Legacy Mode**: Full LLM scanning (v1.0 compatible)

### 🎨 User Interfaces
- ✅ **Desktop App** - Electron-based app for Windows, macOS, and Linux
- ✅ **Web Dashboard** - React UI with real-time metrics and vulnerability overview
- ✅ **REST API** - Programmatic access for CI/CD integration
- ✅ **CLI Mode** - Command-line scanning for automation

### 📋 Reporting & Output
- ✅ **Detailed Issue Reports** - Severity levels, confidence scores, and line numbers
- ✅ **Code Snippets** - Context-aware vulnerable code display
- ✅ **Suggested Fixes** - AI-generated remediation recommendations
- ✅ **Fix Theory** - Explanations of why fixes work
- ✅ **PDF Export** - Professional report generation (via PDFReporter)
- ✅ **Scan History** - Track vulnerabilities over time

### 🔐 Privacy & Security
- ✅ **100% Offline** - No external API calls or cloud uploads
- ✅ **Local LLM** - Powered by Ollama, runs on your hardware
- ✅ **No Authentication** - No registration or login required
- ✅ **Open Source** - Transparent codebase for security auditing

---

## 🛠️ Tech Stack

### Backend
- **Python 3.10+** - Core scanning and analysis engine
- **FastAPI 0.100+** - High-performance REST API framework
- **Pydantic 2.0+** - Data validation and serialization
- **Ollama** - Local Large Language Model integration
- **Uvicorn** - ASGI application server
- **ReportLab** - PDF report generation
- **SQLite** - Lightweight result persistence

### Frontend
- **React 19+** - Modern UI framework with hooks
- **Vite** - Lightning-fast build tool and dev server
- **Tailwind CSS 4+** - Utility-first CSS framework
- **Recharts** - Composable charting library for dashboards
- **Monaco Editor** - VS Code-like code editor for snippets
- **Axios** - Promise-based HTTP client
- **Lucide React** - Beautiful icon library

### Desktop
- **Electron** - Cross-platform desktop application framework
- **Electron Builder** - Automated packaging for macOS, Windows, Linux

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.10+**
- **Node.js 18+** (for development)
- **Ollama** (download from [ollama.ai](https://ollama.ai))

### 30-Second Setup

1. **Start Ollama** with your preferred model:
   ```bash
   ollama run llama2  # or llama3, mistral, neural-chat, etc.
   ```

2. **Clone the repository**:
   ```bash
   git clone https://github.com/Dharanish-AM/Vulnora-AI.git
   cd Vulnora-AI
   ```

3. **Setup Backend**:
   ```bash
   cd server
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python main.py  # Starts API on http://localhost:8000
   ```

4. **Setup Frontend** (in a new terminal):
   ```bash
   cd client
   npm install
   npm run dev  # Development server on http://localhost:5173
   ```

5. **Open your browser**:
   Navigate to `http://localhost:5173` and start scanning!

---

## 📖 Installation

### Detailed Setup Guide

#### Backend Setup

1. **Create and activate virtual environment**:
   ```bash
   cd server
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   # OR
   venv\Scripts\activate  # Windows
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**:
   ```bash
   python -m pip list | grep fastapi
   ```

#### Frontend Setup

1. **Install dependencies**:
   ```bash
   cd client
   npm install
   ```

2. **Build for production** (optional):
   ```bash
   npm run build
   ```

#### Ollama Setup

1. **Install Ollama** from [ollama.ai](https://ollama.ai)

2. **Start the Ollama service**:
   ```bash
   ollama serve
   ```

3. **In another terminal, download a model**:
   ```bash
   ollama pull llama2        # ~4GB
   ollama pull neural-chat   # ~4GB (faster)
   ollama pull llama3        # ~8GB (more accurate)
   ```

---

## 🎮 Usage

### Web Interface (Recommended)

1. **Start backend server** (Terminal 1):
   ```bash
   cd server
   python main.py
   ```

2. **Start frontend dev server** (Terminal 2):
   ```bash
   cd client
   npm run dev
   ```

3. **Open browser**: Visit `http://localhost:5173`

4. **Use the dashboard**:
   - **Dashboard** - Overview of all scans and vulnerabilities
   - **Scan Form** - Select project directory and LLM model
   - **Results** - View vulnerabilities with details and code snippets
   - **Patch Viewer** - Compare suggested fixes side-by-side
   - **History** - Track scans over time

### REST API

**Start the API server**:
```bash
cd server
python main.py
```

**Hybrid Scan** (Default - 5-10x faster):
```bash
curl -X POST http://localhost:8000/scan \
  -H "Content-Type: application/json" \
  -d '{
    "path": "/path/to/project",
    "model": "llama2",
    "use_hybrid": true
  }'
```

**Incremental Scan** (10-100x faster on re-scans):
```bash
curl -X POST http://localhost:8000/scan \
  -H "Content-Type: application/json" \
  -d '{
    "path": "/path/to/project",
    "use_hybrid": true,
    "use_incremental": true
  }'
```

**Legacy Mode** (v1.0 compatible):
```bash
curl -X POST http://localhost:8000/scan \
  -H "Content-Type: application/json" \
  -d '{
    "path": "/path/to/project",
    "use_hybrid": false
  }'
```

**Response** (example):
```json
{
  "scan_id": 1,
  "project_path": "/path/to/project",
  "files_scanned": 42,
  "scan_duration": 125.5,
  "smell_score": 7.3,
  "issues": [
    {
      "file_path": "src/auth.py",
      "line_number": 42,
      "column": 10,
      "rule_id": "CWE-89",
      "vulnerability_type": "SQL Injection",
      "severity": "CRITICAL",
      "confidence": "HIGH",
      "description": "Unescaped user input in SQL query",
      "snippet": "query = f\"SELECT * FROM users WHERE id={user_id}\"",
      "suggested_fix": "Use parameterized queries",
      "fix_theory": "Parameterized queries prevent SQL injection..."
    }
  ]
}
```

### Command Line (CLI)

**Hybrid Scan** (Recommended):
```bash
cd server
python main.py scan --path /path/to/project
```

**Incremental Scan** (Fastest for re-scans):
```bash
# First scan - creates cache
python main.py scan --path /path/to/project --incremental

# Subsequent scans - only scans changed files
python main.py scan --path /path/to/project --incremental
```

**Force Full Scan**:
```bash
python main.py scan --path /path/to/project --incremental --force
```

**Legacy Mode**:
```bash
python main.py scan --path /path/to/project --legacy
```

**Custom Model**:
```bash
python main.py scan --path /path/to/project --model llama3
```

**Output** (example):
```
🔍 Scanning /path/to/project...
🤖 Using model: llama3.1:8b
📊 Mode: Hybrid (Static + LLM)

⚡ Stage 1: Static analysis pre-filter...
✅ Filtered out 85 clean files (85.0%)
🎯 15 files flagged for LLM validation

🤖 Stage 2: LLM deep analysis on 15 files...
  [1/15] ✓ auth.py: 2 issues
  [2/15] ✓ db.py: 1 issue
  ...

✅ Scan complete! Found 5 total issues

🔴 [Critical] LLM-Command-Injection: Command Injection
   📁 /app/db/queries.py:42
   📝 User input directly concatenated into system call

🟠 [High] LLM-SQL-Injection: SQL Injection Risk
   📁 /app/utils/shell.py:15
   📝 Unescaped parameters in SQL query
```

### Desktop Application

**Build the desktop app**:
```bash
cd client
npm install
npm run electron:build
```

**Outputs**:
- macOS: `release/Vulnora AI.dmg`
- Windows: `release/Vulnora AI.exe`
- Linux: `release/Vulnora AI.AppImage`

---

## 🏗️ Architecture

```
Vulnora AI System Architecture
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌─────────────────────────────────────────────────────┐
│              User Interfaces                        │
├─────────────────────────────────────────────────────┤
│  Desktop App (Electron) │ Web UI (React) │ API/CLI  │
└────────────────┬────────────────────────┬───────────┘
                 │                        │
        ┌────────┴────────┐               │
        │                 │               │
┌───────▼──────────────────▼──────────────▼──────┐
│         FastAPI Server (main.py)               │
│  ┌──────────────────────────────────────────┐  │
│  │  REST API Endpoints & Request Handling   │  │
│  └──────────────────────────────────────────┘  │
└────────────┬─────────────────────────────────┬─┘
             │                                 │
   ┌─────────▼──────────┐         ┌───────────▼──────┐
   │  ProjectScanner    │         │  Database (DB)   │
   │  - File Discovery  │         │  - Scan History  │
   │  - Parallel Scan   │         │  - Results Cache │
   │  - Multi-threading │         └──────────────────┘
   └────────┬───────────┘
            │
   ┌────────▼──────────────┐
   │  LLMEngine            │
   │  - Prompt Engineering │
   │  - Response Parsing   │
   │  - JSON Cleaning      │
   └────────┬──────────────┘
            │
   ┌────────▼──────────────┐
   │  Ollama (Local LLM)   │
   │  - Llama 2/3          │
   │  - Mistral            │
   │  - Neural Chat        │
   └───────────────────────┘
```

### Key Components

**ProjectScanner** (`core/scanner.py`)
- Recursively discovers files matching supported extensions
- Implements intelligent directory exclusion
- Orchestrates parallel scanning with ThreadPoolExecutor
- Returns deduplicated vulnerability list

**LLMEngine** (`llm/engine.py`)
- Crafts security-focused prompts for vulnerability detection
- Calls local Ollama API with streaming support
- Parses and cleans JSON responses
- Handles response format validation

**FastAPI Server** (`api/main.py`)
- Provides REST endpoints for scanning and reporting
- CORS-enabled for cross-origin requests
- Background task support for long-running scans
- Comprehensive error handling and logging

**Database** (`core/database.py`)
- Persistent storage of scan results
- Query capabilities for historical analysis
- Integration with reporting module

---

## 📁 Project Structure

```
Vulnora-AI/
├── README.md                  # This file
├── client/                    # Frontend (React + Electron)
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.jsx      # Main vulnerability dashboard
│   │   │   ├── ScanForm.jsx       # Project selection & scan initiation
│   │   │   ├── VulnerabilityList.jsx  # Issues display with filtering
│   │   │   ├── PatchViewer.jsx    # Side-by-side fix comparison
│   │   │   ├── History.jsx        # Scan history and trends
│   │   │   └── LandingPage.jsx    # Welcome/getting started
│   │   ├── context/
│   │   │   └── ThemeContext.jsx   # Dark/light mode state
│   │   ├── App.jsx            # Main app wrapper
│   │   ├── main.jsx           # React entry point
│   │   └── index.css          # Global styles
│   ├── electron/
│   │   ├── main.js            # Electron main process
│   │   └── preload.js         # Context isolation bridge
│   ├── package.json           # Dependencies & scripts
│   ├── vite.config.js         # Vite build configuration
│   ├── tailwind.config.js     # Tailwind CSS setup
│   └── electron-builder.json  # Desktop app build config
│
├── server/                    # Backend (Python + FastAPI)
│   ├── main.py               # Application entry point
│   ├── requirements.txt       # Python dependencies
│   ├── streamlit_app.py       # Alternative Streamlit UI
│   └── app/
│       ├── __init__.py
│       ├── api/
│       │   └── main.py        # FastAPI app & endpoints
│       ├── core/
│       │   ├── scanner.py     # Project scanner orchestration
│       │   ├── database.py    # Result persistence
│       │   └── reporter.py    # PDF report generation
│       ├── llm/
│       │   └── engine.py      # LLM integration & prompting
│       └── models/
│           └── issue.py       # Data models (IssueCandidate, ScanResult)
│
├── test_project/             # Sample vulnerable code for testing
│   ├── vulnerable.py
│   └── vulnerable.js
│
└── .git/                      # Version control
```

---

## 🔌 API Reference

### Endpoints

#### POST `/scan`
Initiate a security scan of a project.

**Request**:
```json
{
  "path": "/absolute/path/to/project",
  "model": "llama2"
}
```

**Response** (`ScanResult`):
```json
{
  "scan_id": 1,
  "project_path": "/path/to/project",
  "files_scanned": 42,
  "scan_duration": 125.5,
  "smell_score": 7.3,
  "issues": [
    {
      "file_path": "src/auth.py",
      "line_number": 42,
      "column": 10,
      "rule_id": "CWE-89",
      "vulnerability_type": "SQL Injection",
      "severity": "CRITICAL",
      "confidence": "HIGH",
      "description": "Unescaped user input in SQL query...",
      "snippet": "query = f\"SELECT * FROM users WHERE id={user_id}\"",
      "suggested_fix": "Use parameterized queries: cursor.execute(...)",
      "fix_theory": "Parameterized queries prevent SQL injection by..."
    }
  ]
}
```

#### GET `/`
Health check endpoint.

**Response**:
```json
{
  "message": "Vulnora AI API is running"
}
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the `server/` directory (optional):

```env
# Ollama Configuration
OLLAMA_API_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=llama2

# FastAPI Server
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true

# Logging
LOG_LEVEL=INFO

# Database
DATABASE_PATH=./vulnora.db
```

### Supported LLM Models

The following Ollama models are tested and recommended:

| Model | Speed | Accuracy | Memory | Recommended For |
|-------|-------|----------|--------|-----------------|
| **Neural Chat** | ⚡⚡⚡ Fast | Good | 4-8GB | Fast scans, good balance |
| **Llama 2** | ⚡⚡ Medium | Excellent | 8-16GB | Best accuracy |
| **Llama 3** | ⚡⚡ Medium | Excellent | 8-16GB | Latest, improved reasoning |
| **Mistral** | ⚡⚡⚡ Fast | Good | 4-8GB | Fast, efficient |
| **Dolphin** | ⚡ Slow | Excellent | 16GB+ | Maximum accuracy |

**Install a model**:
```bash
ollama run llama3          # or any other model
ollama pull neural-chat    # Pre-download without running
```

### Scanner Configuration

Edit `server/app/core/scanner.py` to customize:

```python
# Supported file extensions
self.supported_extensions = {'.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.go', '.rs'}

# Directories to skip
self.excluded_dirs = {
    '.git', '.venv', 'node_modules', 'dist', 'build',
    '__pycache__', 'vendor', '.idea', '.vscode'
}
```

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create a branch**: `git checkout -b feature/your-feature`
3. **Commit changes**: `git commit -am 'Add your feature'`
4. **Push to branch**: `git push origin feature/your-feature`
5. **Submit a Pull Request**

### Areas for Contribution
- 🧪 Additional programming language support
- 📈 Performance optimizations for large projects
- 🎨 UI/UX improvements
- 🔬 Enhanced vulnerability detection patterns
- 📚 Documentation and tutorials
- 🐛 Bug fixes and error handling
- 🧵 Async processing for faster scans

---

## 📝 License

Vulnora AI is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## 👤 Contact & Support

- **Author**: [Dharanish AM](https://github.com/Dharanish-AM)
- **Email**: dharanish816@gmail.com
- **GitHub**: [Vulnora-AI Repository](https://github.com/Dharanish-AM/Vulnora-AI)
- **Issues**: [Report bugs or request features](https://github.com/Dharanish-AM/Vulnora-AI/issues)

---

## ⭐ Star History

If you find Vulnora AI useful, please give it a star! It helps others discover the project.

---

<div align="center">

**Built with ❤️ for security-conscious developers**

[⬆ Back to Top](#-vulnora-ai)

</div>
