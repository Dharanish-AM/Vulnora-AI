# 🛡️ Vulnora AI

**AI-Powered Multi-Language Security Scanner with Real-Time Vulnerability Detection**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/React-19.2.0-61DAFB.svg?logo=react)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Environment Variables](#-environment-variables)
- [Usage](#-usage)
  - [CLI Mode](#cli-mode)
  - [API Mode](#api-mode)
  - [Web Interface](#web-interface)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

---

## 🎯 Overview

Vulnora AI is an **enterprise-grade, offline security scanner** that analyzes software projects for vulnerabilities using a hybrid approach combining:

- **Static Analysis** - Pattern-based vulnerability detection
- **AST Taint Analysis** - Data flow tracking for Python
- **LLM Validation** - AI-powered verification using local models (Ollama)

### Why Vulnora AI?

**Problem**: Traditional security scanners either produce too many false positives or require cloud uploads, compromising code privacy.

**Solution**: Vulnora AI runs entirely on your local machine, uses AI to validate findings, and provides actionable fixes—all while keeping your code private.

### Who Is It For?

- **Security Engineers** - Integrate into CI/CD pipelines
- **Development Teams** - Catch vulnerabilities before production
- **Solo Developers** - Quick security audits without cloud dependencies
- **Enterprises** - Maintain code privacy with offline scanning

---

## ✨ Features

### Core Capabilities

- ✅ **Multi-Language Support** - Python, JavaScript, TypeScript, Java, Go, Rust, C/C++
- ✅ **Hybrid Analysis Engine**
  - Regex pattern matching for known vulnerabilities
  - AST-based taint analysis for Python
  - LLM validation to reduce false positives
- ✅ **High Performance**
  - Parallel file scanning with multi-threading
  - Smart directory exclusion (node_modules, .venv, etc.)
  - Optimized for large codebases
- ✅ **100% Offline & Private** - No cloud uploads, runs locally
- ✅ **Modern Web UI** - React-based dashboard with real-time metrics
- ✅ **REST API** - Easy integration into existing workflows
- ✅ **CLI Support** - Scan projects from the command line
- ✅ **Detailed Reports** - Vulnerability descriptions, severity levels, and suggested fixes

### Security Checks

- 🔒 Hardcoded secrets and API keys
- 💉 SQL injection vulnerabilities
- 🚨 Command injection risks
- 🔓 Insecure deserialization
- ⚠️ XSS (Cross-Site Scripting)
- 🛡️ Path traversal vulnerabilities
- 🔐 Weak cryptographic practices
- 📊 And more...

---

## 🛠️ Tech Stack

### Backend
- **Python 3.10+** - Core scanning engine
- **FastAPI** - REST API framework
- **Pydantic** - Data validation
- **Ollama** - Local LLM integration
- **Uvicorn** - ASGI server

### Frontend
- **React 19** - UI framework
- **Vite** - Build tool
- **Tailwind CSS 4** - Styling
- **Recharts** - Data visualization
- **Monaco Editor** - Code display
- **Axios** - HTTP client

### Additional Tools
- **Streamlit** - Alternative standalone UI
- **Rich** - Terminal formatting
- **Lucide React** - Icon library

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Vulnora AI System                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐      ┌──────────────┐                   │
│  │ React Client │◄────►│  FastAPI     │                   │
│  │   (Port      │      │  Backend     │                   │
│  │    5173)     │      │  (Port 8000) │                   │
│  └──────────────┘      └──────┬───────┘                   │
│                               │                            │
│                               ▼                            │
│                    ┌──────────────────┐                   │
│                    │ Scanner Engine   │                   │
│                    │  - File Discovery│                   │
│                    │  - Parallel Scan │                   │
│                    └────────┬─────────┘                   │
│                             │                              │
│         ┌───────────────────┼───────────────────┐         │
│         ▼                   ▼                   ▼         │
│  ┌─────────────┐   ┌──────────────┐   ┌──────────────┐  │
│  │   Regex     │   │  SAST/AST    │   │    Taint     │  │
│  │   Scanner   │   │   Analyzer   │   │   Analyzer   │  │
│  └─────────────┘   └──────────────┘   └──────────────┘  │
│         │                   │                   │         │
│         └───────────────────┼───────────────────┘         │
│                             ▼                              │
│                    ┌──────────────────┐                   │
│                    │   LLM Engine     │                   │
│                    │   (Ollama)       │                   │
│                    └──────────────────┘                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Workflow

1. **File Discovery** - Recursively scans project directories
2. **Parallel Analysis** - Runs regex, SAST, and taint analysis concurrently
3. **LLM Validation** - High-severity issues verified by local AI
4. **Deduplication** - Removes duplicate findings
5. **Report Generation** - Creates detailed vulnerability reports

---

## 📦 Installation

### Prerequisites

- **Python 3.10+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **Ollama** - [Install](https://ollama.com/)

### Step 1: Clone the Repository

```bash
git clone https://github.com/Dharanish-AM/Vulnora-AI.git
cd Vulnora-AI
```

### Step 2: Backend Setup

```bash
cd server
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Step 3: Frontend Setup

```bash
cd ../client
npm install
```

### Step 4: Install Ollama Model

```bash
ollama pull llama3.1:8b
# Or use: llama3, mistral, codellama
```

---

## 🔐 Environment Variables

Currently, Vulnora AI works out-of-the-box with default settings. Optional configurations:

| Variable | Description | Default |
|----------|-------------|---------|
| `OLLAMA_HOST` | Ollama API endpoint | `http://localhost:11434` |
| `API_PORT` | FastAPI server port | `8000` |
| `LOG_LEVEL` | Logging verbosity | `INFO` |

Create a `.env` file in the `server/` directory if customization is needed.

---

## 🚀 Usage

### CLI Mode

Scan a project directly from the command line:

```bash
cd server
source .venv/bin/activate
python main.py scan --path /path/to/your/project
```

**Output:**
```
Scanning /path/to/your/project...

Scan complete. Found 5 issues.
[Critical] PY-AST-002: subprocess call with shell=True - vulnerable.py:14
[High] PY-001: Hardcoded secret detected - vulnerable.py:10
[High] JS-001: Hardcoded secret detected - vulnerable.js:2
[Critical] JS-002: Use of eval() is dangerous - vulnerable.js:6
[Medium] JS-003: Potential XSS via innerHTML - vulnerable.js:9
```

### API Mode

Start the FastAPI backend:

```bash
cd server
source .venv/bin/activate
python main.py api
# Or simply: python main.py
```

Server runs at `http://localhost:8000`

### Web Interface

#### Option 1: React Client (Recommended)

```bash
# Terminal 1: Start backend
cd server
source .venv/bin/activate
python main.py

# Terminal 2: Start frontend
cd client
npm run dev
```

Open `http://localhost:5173`

#### Option 2: Streamlit (Standalone)

```bash
cd server
streamlit run streamlit_app.py
```

Open `http://localhost:8501`

---

## 📡 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### `POST /scan`

Scan a project for vulnerabilities.

**Request:**
```json
{
  "project_path": "/absolute/path/to/project",
  "llm_model": "gemini"
}
```

**Response:**
```json
{
  "project_path": "/path/to/project",
  "issues": [
    {
      "file_path": "vulnerable.py",
      "line_number": 14,
      "column": 5,
      "rule_id": "PY-AST-002",
      "vulnerability_type": "Command Injection",
      "severity": "Critical",
      "description": "subprocess call with shell=True is vulnerable...",
      "confidence": "High",
      "snippet": "subprocess.call(cmd, shell=True)",
      "suggested_fix": "subprocess.call(shlex.split(cmd))",
      "fix_theory": "Use shlex.split() to safely parse commands..."
    }
  ],
  "smell_score": 85.5,
  "scan_duration": 2.34,
  "files_scanned": 42
}
```

#### `GET /health`

Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

---

## 📂 Project Structure

```
Vulnora-AI/
├── client/                     # React Frontend
│   ├── src/
│   │   ├── components/         # React components
│   │   │   ├── Dashboard.jsx   # Metrics dashboard
│   │   │   ├── LandingPage.jsx # Home page
│   │   │   └── VulnerabilityList.jsx
│   │   ├── context/            # React context
│   │   ├── App.jsx             # Main app component
│   │   └── index.css           # Global styles
│   ├── package.json
│   └── vite.config.js
│
├── server/                     # Python Backend
│   ├── main.py                 # CLI entry point
│   ├── streamlit_app.py        # Streamlit UI
│   ├── requirements.txt
│   └── vulnora/                # Core package
│       ├── api/                # FastAPI routes
│       │   └── main.py
│       ├── core/               # Scanning logic
│       │   ├── scanner.py      # Main scanner
│       │   └── patterns.py     # Vulnerability patterns
│       ├── scanners/           # Analysis engines
│       │   ├── regex.py        # Pattern matching
│       │   └── sast.py         # AST analysis
│       ├── analyzers/          # Advanced analyzers
│       │   └── taint.py        # Taint tracking
│       ├── llm/                # LLM integration
│       │   └── engine.py
│       └── models/             # Data models
│           └── issue.py
│
└── test_project/               # Test cases
    ├── vulnerable.py
    └── vulnerable.js
```

---

## 🗺️ Roadmap

### ✅ Completed
- [x] Multi-language support (Python, JS, TS, Java, Go, Rust, C/C++)
- [x] Parallel scanning engine
- [x] LLM integration with Ollama
- [x] React web interface
- [x] REST API
- [x] CLI support

### 🚧 In Progress
- [ ] GitHub Actions integration
- [ ] Docker containerization
- [ ] VS Code extension

### 📋 Planned Features

**Q1 2025**
- [ ] GitLab CI/CD integration
- [ ] SARIF report format
- [ ] Custom rule definitions
- [ ] Severity threshold configuration

**Q2 2025**
- [ ] Multi-repository scanning
- [ ] Historical scan comparison
- [ ] Automated fix suggestions (PR creation)
- [ ] Integration with Jira/Linear

**Q3 2025**
- [ ] Support for more languages (PHP, Ruby, Kotlin)
- [ ] Machine learning-based pattern detection
- [ ] Cloud deployment option (self-hosted)

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

### How to Contribute

1. **Fork the repository**
   ```bash
   git clone https://github.com/Dharanish-AM/Vulnora-AI.git
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make your changes**
   - Follow existing code style
   - Add tests if applicable
   - Update documentation

4. **Commit your changes**
   ```bash
   git commit -m "feat: add amazing feature"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```

6. **Open a Pull Request**

### Development Guidelines

- Write clear commit messages
- Add tests for new features
- Update README if needed
- Ensure all tests pass
- Follow Python PEP 8 and React best practices

---

## 📄 License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for more information.

---

## 📧 Contact

**Dharanish AM**

- 📧 Email: [dharanish816@gmail.com](mailto:dharanish816@gmail.com)
- 💼 LinkedIn: [linkedin.com/in/dharanish-am](https://www.linkedin.com/in/dharanish-a-m-40a797295/)
- 🐙 GitHub: [@Dharanish-AM](https://github.com/Dharanish-AM)
- 🌐 Portfolio: [portfolio-amd.vercel.app](https://portfolio-amd.vercel.app/)

---

<div align="center">

**⭐ If you find Vulnora AI useful, please consider giving it a star!**

Made with ❤️ by [Dharanish AM](https://github.com/Dharanish-AM)

</div>
