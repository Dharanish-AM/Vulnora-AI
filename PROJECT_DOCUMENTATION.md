# Vulnora AI - Complete Project Documentation

> **A Comprehensive Study Guide for Understanding Every Aspect of the Project**

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Backend Deep Dive](#backend-deep-dive)
4. [Frontend Deep Dive](#frontend-deep-dive)
5. [Electron Desktop App](#electron-desktop-app)
6. [Security Scanning Engine](#security-scanning-engine)
7. [Data Flow](#data-flow)
8. [Development Workflow](#development-workflow)
9. [Key Concepts](#key-concepts)
10. [File-by-File Breakdown](#file-by-file-breakdown)

---

## 1. Project Overview

### What is Vulnora AI?

Vulnora AI is an **AI-powered security vulnerability scanner** that analyzes source code to detect security issues. It's a full-stack application with:

- **Desktop Application** (Electron + React)
- **Web Interface** (React + Vite)
- **Backend API** (Python + FastAPI)
- **CLI Tool** (Python)
- **Alternative UI** (Streamlit)

### Core Value Proposition

**Problem**: Traditional security scanners produce too many false positives or require cloud uploads (privacy concerns).

**Solution**: Vulnora AI runs entirely offline, uses AI to validate findings, and provides actionable fixes while keeping code private.

### Technology Stack

```
Frontend:
├── React 19 (UI framework)
├── Vite 7 (Build tool)
├── Tailwind CSS 4 (Styling)
├── Electron 39 (Desktop app)
├── Monaco Editor (Code display)
├── Recharts (Data visualization)
├── Axios (HTTP client)
└── Lucide React (Icons)

Backend:
├── Python 3.10+
├── FastAPI (REST API)
├── Uvicorn (ASGI server)
├── Pydantic (Data validation)
├── Ollama (Local LLM)
└── AST (Abstract Syntax Tree analysis)
```

---

## 2. System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    VULNORA AI SYSTEM                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────┐         ┌──────────────────┐        │
│  │  Electron App    │◄───────►│  React Web App   │        │
│  │  (Desktop)       │         │  (Browser)       │        │
│  └────────┬─────────┘         └────────┬─────────┘        │
│           │                            │                   │
│           └────────────┬───────────────┘                   │
│                        │                                    │
│                        ▼                                    │
│           ┌────────────────────────┐                       │
│           │   FastAPI Backend      │                       │
│           │   (localhost:8000)     │                       │
│           └───────────┬────────────┘                       │
│                       │                                     │
│                       ▼                                     │
│           ┌────────────────────────┐                       │
│           │   Scanner Engine       │                       │
│           │   - File Discovery     │                       │
│           │   - Parallel Scanning  │                       │
│           └───────────┬────────────┘                       │
│                       │                                     │
│       ┌───────────────┼───────────────┐                   │
│       ▼               ▼               ▼                   │
│  ┌─────────┐   ┌──────────┐   ┌──────────┐              │
│  │ Regex   │   │   SAST   │   │  Taint   │              │
│  │ Scanner │   │ Analyzer │   │ Analyzer │              │
│  └─────────┘   └──────────┘   └──────────┘              │
│       │               │               │                   │
│       └───────────────┼───────────────┘                   │
│                       ▼                                     │
│           ┌────────────────────────┐                       │
│           │   LLM Engine (Ollama)  │                       │
│           │   - Validates findings │                       │
│           │   - Reduces false +    │                       │
│           └────────────────────────┘                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Component Interaction

1. **User Interface Layer**
   - Electron Desktop App OR React Web App
   - Collects project path and scan parameters
   - Displays results with visualizations

2. **API Layer**
   - FastAPI handles HTTP requests
   - Validates input data
   - Orchestrates scanning process
   - Returns structured results

3. **Scanning Engine**
   - Discovers files in project
   - Runs multiple analyzers in parallel
   - Deduplicates findings
   - Calculates "smell score"

4. **Analysis Layer**
   - **Regex Scanner**: Pattern matching for known vulnerabilities
   - **SAST Analyzer**: AST-based static analysis (Python only)
   - **Taint Analyzer**: Data flow tracking (Python only)

5. **AI Validation Layer**
   - Ollama LLM validates high-severity findings
   - Reduces false positives
   - Generates fix suggestions

---

## 3. Backend Deep Dive

### Directory Structure

```
server/
├── main.py                    # Entry point (CLI + API launcher)
├── requirements.txt           # Python dependencies
├── streamlit_app.py          # Alternative Streamlit UI
└── vulnora/                  # Main package
    ├── __init__.py
    ├── api/                  # FastAPI routes
    │   ├── __init__.py
    │   └── main.py          # API endpoints
    ├── core/                 # Core scanning logic
    │   ├── __init__.py
    │   ├── scanner.py       # Main scanner orchestrator
    │   └── patterns.py      # Vulnerability patterns
    ├── scanners/             # Individual scanners
    │   ├── __init__.py
    │   ├── regex.py         # Pattern-based scanner
    │   └── sast.py          # AST-based scanner
    ├── analyzers/            # Advanced analyzers
    │   ├── __init__.py
    │   └── taint.py         # Taint analysis
    ├── llm/                  # LLM integration
    │   ├── __init__.py
    │   └── engine.py        # Ollama client
    ├── models/               # Data models
    │   ├── __init__.py
    │   └── issue.py         # Issue/vulnerability model
    └── utils/                # Utilities
        └── __init__.py
```

### Key Backend Files

#### `main.py` - Entry Point

```python
# Responsibilities:
# 1. Parse command-line arguments
# 2. Start API server OR run CLI scan
# 3. Handle different modes (api, scan)

# Modes:
# - api: Starts FastAPI server on port 8000
# - scan: Runs CLI scan on specified path
```

**Key Functions:**
- `start_api()`: Launches Uvicorn server with hot-reload
- `main()`: Argument parser and mode dispatcher

#### `vulnora/api/main.py` - FastAPI Application

```python
# Responsibilities:
# 1. Define API endpoints
# 2. Handle CORS for frontend
# 3. Validate request/response data
# 4. Orchestrate scanning process

# Endpoints:
# - POST /scan: Trigger vulnerability scan
# - GET /health: Health check
```

**Key Components:**
- `app`: FastAPI application instance
- CORS middleware for cross-origin requests
- Request/response models using Pydantic

#### `vulnora/core/scanner.py` - Scanner Orchestrator

```python
# Responsibilities:
# 1. Discover files in project directory
# 2. Filter out excluded directories (node_modules, .venv, etc.)
# 3. Run multiple scanners in parallel
# 4. Deduplicate findings
# 5. Calculate smell score
# 6. Validate with LLM

# Key Methods:
# - discover_files(): Recursively find scannable files
# - scan(): Main scanning orchestration
# - _run_parallel_analysis(): Multi-threaded scanning
# - _deduplicate_issues(): Remove duplicate findings
# - _calculate_smell_score(): Risk assessment
```

**Scanning Workflow:**
1. Discover all files (exclude `.venv`, `node_modules`, `.git`, etc.)
2. Determine language for each file
3. Run appropriate scanners in parallel threads
4. Collect all findings
5. Deduplicate based on file+line+rule_id
6. Validate high-severity issues with LLM
7. Calculate overall smell score
8. Return structured results

#### `vulnora/core/patterns.py` - Vulnerability Patterns

```python
# Responsibilities:
# 1. Define regex patterns for each vulnerability type
# 2. Map patterns to severity levels
# 3. Provide descriptions and fix suggestions

# Pattern Structure:
# {
#     'rule_id': 'PY-001',
#     'pattern': r'regex_pattern',
#     'severity': 'High',
#     'description': 'What the vulnerability is',
#     'suggested_fix': 'How to fix it'
# }
```

**Supported Languages:**
- Python (PY-*)
- JavaScript/TypeScript (JS-*)
- Java (JAVA-*)
- Go (GO-*)
- Rust (RUST-*)
- C/C++ (C-*)

#### `vulnora/scanners/regex.py` - Pattern Scanner

```python
# Responsibilities:
# 1. Apply regex patterns to code
# 2. Extract code snippets
# 3. Create Issue objects for matches

# How it works:
# - Loads patterns from patterns.py
# - Iterates through each pattern
# - Searches file content with regex
# - Captures line number and context
# - Returns list of Issue objects
```

#### `vulnora/scanners/sast.py` - AST Scanner

```python
# Responsibilities:
# 1. Parse Python code into AST
# 2. Analyze AST nodes for vulnerabilities
# 3. Detect dangerous function calls
# 4. Find insecure patterns

# Checks:
# - subprocess with shell=True
# - eval() usage
# - exec() usage
# - pickle.loads()
# - yaml.load() without SafeLoader
```

**How AST Works:**
```python
# Code: subprocess.call(cmd, shell=True)
# AST: Call(func=Attribute(value=Name(id='subprocess'), attr='call'))
# Detection: Check if 'shell' keyword arg is True
```

#### `vulnora/analyzers/taint.py` - Taint Analysis

```python
# Responsibilities:
# 1. Track data flow from sources to sinks
# 2. Detect SQL injection paths
# 3. Find command injection vulnerabilities

# Concepts:
# - Source: User input (request.args, input(), etc.)
# - Sink: Dangerous function (execute(), os.system(), etc.)
# - Taint: Data flows from source to sink without sanitization
```

**Example:**
```python
# Source
user_input = request.args.get('id')

# Sink (vulnerable if tainted)
db.execute(f"SELECT * FROM users WHERE id = {user_input}")
```

#### `vulnora/llm/engine.py` - LLM Integration

```python
# Responsibilities:
# 1. Connect to Ollama API
# 2. Validate vulnerability findings
# 3. Generate fix theories
# 4. Reduce false positives

# Process:
# 1. Format issue as prompt
# 2. Send to Ollama (llama3.1:8b)
# 3. Parse AI response
# 4. Extract validation + fix theory
# 5. Update issue object
```

#### `vulnora/models/issue.py` - Data Model

```python
# Issue Model Fields:
# - file_path: Where vulnerability is
# - line_number: Exact line
# - column: Column position
# - rule_id: Pattern identifier
# - vulnerability_type: Category
# - severity: Critical/High/Medium/Low
# - description: What's wrong
# - confidence: High/Medium/Low
# - snippet: Code context
# - suggested_fix: How to fix
# - fix_theory: Why fix works
```

---

## 4. Frontend Deep Dive

### Directory Structure

```
client/
├── index.html                # Entry HTML
├── package.json              # Dependencies
├── vite.config.js           # Vite configuration
├── tailwind.config.js       # Tailwind CSS config
├── electron/                 # Electron files
│   ├── main.js              # Main process
│   └── preload.js           # Preload script
├── public/                   # Static assets
└── src/
    ├── main.jsx             # React entry point
    ├── App.jsx              # Root component
    ├── index.css            # Global styles
    ├── components/          # React components
    │   ├── LandingPage.jsx
    │   ├── ScanForm.jsx
    │   ├── Dashboard.jsx
    │   ├── VulnerabilityList.jsx
    │   └── PatchViewer.jsx
    ├── context/             # React context
    │   └── ThemeContext.jsx
    └── lib/                 # Utilities
```

### Key Frontend Files

#### `src/main.jsx` - React Entry

```javascript
// Responsibilities:
// 1. Mount React app to DOM
// 2. Wrap app with providers (ThemeProvider)
// 3. Enable StrictMode for development

// Flow:
// ReactDOM.createRoot() → ThemeProvider → App
```

#### `src/App.jsx` - Root Component

```javascript
// State Management:
// - showLanding: Toggle landing page
// - result: Scan results from API
// - isLoading: Loading state
// - error: Error messages
// - theme: Light/dark mode

// Key Functions:
// - handleScan(): POST to /api/scan
// - Manages UI flow (landing → scan → results)

// Component Tree:
// App
// ├── Header (Shield icon + title + theme toggle)
// ├── LandingPage (if showLanding)
// └── Main Content
//     ├── ScanForm
//     ├── Error Display
//     └── Results
//         ├── Dashboard
//         └── VulnerabilityList
```

#### `src/components/LandingPage.jsx`

```javascript
// Responsibilities:
// 1. Welcome screen
// 2. Feature highlights
// 3. "Start Scanning" CTA

// Design:
// - Hero section with gradient
// - Feature cards (Offline, AI-Powered, Multi-Language)
// - Animated entrance
```

#### `src/components/ScanForm.jsx`

```javascript
// Responsibilities:
// 1. Collect project path
// 2. Select LLM model
// 3. Trigger scan

// Features:
// - Directory picker (Electron API)
// - Model dropdown (llama3.1:8b, gemini, etc.)
// - Loading state with spinner
// - Form validation

// Electron Integration:
// window.electronAPI?.selectDirectory()
```

#### `src/components/Dashboard.jsx`

```javascript
// Responsibilities:
// 1. Display scan metrics
// 2. Show severity breakdown
// 3. Visualize data with charts

// Metrics:
// - Total Issues
// - Smell Score (0-100)
// - Scan Duration
// - Files Scanned

// Charts (Recharts):
// - Severity distribution (pie chart)
// - Issues by type (bar chart)
// - Confidence levels (donut chart)
```

#### `src/components/VulnerabilityList.jsx`

```javascript
// Responsibilities:
// 1. List all vulnerabilities
// 2. Expandable details
// 3. Code display with Monaco Editor

// Structure:
// VulnerabilityList
// └── VulnerabilityItem (for each issue)
//     ├── Header (severity badge + type + location)
//     └── Expanded Details
//         ├── Description
//         ├── Location
//         ├── Code Analysis (Monaco Editor)
//         └── Suggested Fix
//             ├── Theory
//             └── Code (Monaco Editor)

// Monaco Editor:
// - Syntax highlighting
// - Read-only mode
// - Light theme
// - Line numbers off
```

#### `src/context/ThemeContext.jsx`

```javascript
// Responsibilities:
// 1. Manage light/dark theme
// 2. Persist theme in localStorage
// 3. Apply theme class to DOM

// API:
// - theme: 'light' | 'dark'
// - toggleTheme(): Switch theme

// Usage:
// const { theme, toggleTheme } = useTheme();
```

#### `src/index.css` - Global Styles

```css
/* CSS Variables (Design Tokens) */
:root {
  /* Colors */
  --color-primary: #6B3F69;      /* Deep Purple */
  --color-secondary: #2D1A2C;    /* Darker Purple */
  --color-accent: #A376A2;       /* Light Purple */
  
  /* Backgrounds */
  --bg-main: #FAF5F8;            /* Very light purple */
  --bg-card: #FFFFFF;            /* White */
  
  /* Text */
  --text-main: #1A0F19;          /* Dark purple */
  --text-muted: #6B3F69;         /* Muted purple */
  
  /* Borders */
  --border-color: #DDC3C3;       /* Dusty rose */
}

/* Fonts */
--font-sans: 'Poppins', sans-serif;
--font-mono: 'JetBrains Mono', monospace;

/* Utility Classes */
.modern-card {
  /* Card styling with hover effects */
}
```

---

## 5. Electron Desktop App

### Architecture

```
Electron App
├── Main Process (main.js)
│   ├── Window management
│   ├── IPC handlers
│   └── Native dialogs
├── Preload Script (preload.js)
│   └── Context bridge (secure IPC)
└── Renderer Process (React App)
    └── UI components
```

### `electron/main.js` - Main Process

```javascript
// Responsibilities:
// 1. Create BrowserWindow
// 2. Load React app (dev or production)
// 3. Handle IPC communication
// 4. Manage app lifecycle

// Key Functions:
// - createWindow(): Create main window
// - IPC Handlers:
//   - select-directory: Native folder picker
//   - check-server-health: Ping Python server
//   - get-server-url: Return server URL

// Window Configuration:
// - Size: 1400x900
// - Min size: 1200x700
// - Context isolation: true
// - Node integration: false (security)
// - Preload script: preload.js
```

**Security Features:**
- Context isolation prevents renderer from accessing Node.js
- Preload script creates safe bridge
- CSP headers restrict resource loading

### `electron/preload.js` - Preload Script

```javascript
// Responsibilities:
// 1. Expose safe APIs to renderer
// 2. Bridge main ↔ renderer communication
// 3. Maintain security boundaries

// Exposed APIs (window.electronAPI):
// - selectDirectory(): Open folder picker
// - checkServerHealth(): Ping server
// - getServerUrl(): Get server URL
// - isElectron(): Check if running in Electron

// Security:
// - Uses contextBridge.exposeInMainWorld()
// - Only exposes specific functions
// - No direct Node.js access
```

### Electron ↔ React Communication

```javascript
// Renderer (React) → Main Process
const path = await window.electronAPI.selectDirectory();

// Main Process handles IPC
ipcMain.handle('select-directory', async () => {
  const result = await dialog.showOpenDialog({
    properties: ['openDirectory']
  });
  return result.filePaths[0];
});
```

### Build Configuration

```json
// package.json
{
  "main": "dist-electron/main.js",
  "scripts": {
    "electron:dev": "vite",           // Dev mode
    "electron:build": "vite build && electron-builder"
  },
  "build": {
    "appId": "com.dharanish.vulnora-ai",
    "productName": "Vulnora AI",
    "mac": { "target": ["dmg", "zip"] },
    "win": { "target": ["nsis", "portable"] },
    "linux": { "target": ["AppImage", "deb"] }
  }
}
```

---

## 6. Security Scanning Engine

### Scanning Workflow

```
1. File Discovery
   ↓
2. Language Detection
   ↓
3. Parallel Analysis
   ├── Regex Scanner
   ├── SAST Analyzer (Python only)
   └── Taint Analyzer (Python only)
   ↓
4. Collect Findings
   ↓
5. Deduplication
   ↓
6. LLM Validation (High severity)
   ↓
7. Calculate Smell Score
   ↓
8. Return Results
```

### File Discovery Algorithm

```python
def discover_files(project_path):
    # Excluded directories
    EXCLUDED = {
        'node_modules', '.venv', 'venv', '__pycache__',
        '.git', 'dist', 'build', 'target'
    }
    
    # Supported extensions
    EXTENSIONS = {
        '.py', '.js', '.ts', '.jsx', '.tsx',
        '.java', '.go', '.rs', '.c', '.cpp'
    }
    
    # Recursively walk directory
    for root, dirs, files in os.walk(project_path):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in EXCLUDED]
        
        # Collect files with supported extensions
        for file in files:
            if any(file.endswith(ext) for ext in EXTENSIONS):
                yield os.path.join(root, file)
```

### Parallel Analysis

```python
from concurrent.futures import ThreadPoolExecutor

def _run_parallel_analysis(files):
    issues = []
    
    # Create thread pool
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Submit analysis tasks
        futures = [
            executor.submit(analyze_file, file)
            for file in files
        ]
        
        # Collect results
        for future in futures:
            issues.extend(future.result())
    
    return issues
```

### Deduplication Logic

```python
def _deduplicate_issues(issues):
    seen = set()
    unique = []
    
    for issue in issues:
        # Create unique key
        key = (
            issue.file_path,
            issue.line_number,
            issue.rule_id
        )
        
        # Add if not seen
        if key not in seen:
            seen.add(key)
            unique.append(issue)
    
    return unique
```

### Smell Score Calculation

```python
def _calculate_smell_score(issues):
    # Severity weights
    weights = {
        'Critical': 10,
        'High': 7,
        'Medium': 4,
        'Low': 2
    }
    
    # Calculate weighted sum
    total = sum(weights.get(issue.severity, 0) for issue in issues)
    
    # Normalize to 0-100 scale
    # Higher score = more issues
    return min(total, 100)
```

### LLM Validation

```python
def validate_with_llm(issue):
    # Only validate high-severity issues
    if issue.severity not in ['Critical', 'High']:
        return issue
    
    # Create prompt
    prompt = f"""
    Analyze this potential vulnerability:
    
    Code: {issue.snippet}
    Type: {issue.vulnerability_type}
    
    Is this a real vulnerability? Explain why and suggest a fix.
    """
    
    # Call Ollama
    response = ollama.generate(
        model='llama3.1:8b',
        prompt=prompt
    )
    
    # Parse response
    issue.description += f" [AI Analysis: {response}]"
    issue.fix_theory = extract_fix_theory(response)
    
    return issue
```

---

## 7. Data Flow

### Complete Request Flow

```
1. User Input (Frontend)
   ↓
   Project Path: /path/to/project
   Model: llama3.1:8b
   ↓

2. HTTP Request
   ↓
   POST /api/scan
   Body: { "path": "...", "model": "..." }
   ↓

3. FastAPI Handler (Backend)
   ↓
   Validate request
   Create ProjectScanner instance
   ↓

4. Scanner Initialization
   ↓
   Store project_path
   Store llm_model
   ↓

5. File Discovery
   ↓
   Walk directory tree
   Filter by extension
   Exclude node_modules, .venv, etc.
   ↓
   Result: List of file paths
   ↓

6. Parallel Analysis
   ↓
   For each file:
     ├── Detect language
     ├── Run Regex Scanner
     ├── Run SAST (if Python)
     └── Run Taint Analysis (if Python)
   ↓
   Result: List of Issue objects
   ↓

7. Deduplication
   ↓
   Remove duplicate findings
   (same file + line + rule)
   ↓

8. LLM Validation
   ↓
   For Critical/High severity:
     ├── Format prompt
     ├── Call Ollama API
     ├── Parse response
     └── Update issue
   ↓

9. Smell Score Calculation
   ↓
   Weighted sum of severities
   Normalized to 0-100
   ↓

10. Response Formation
    ↓
    {
      "project_path": "...",
      "issues": [...],
      "smell_score": 85.5,
      "scan_duration": 2.34,
      "files_scanned": 42
    }
    ↓

11. HTTP Response
    ↓
    200 OK + JSON body
    ↓

12. Frontend Processing
    ↓
    Parse response
    Update state (setResult)
    ↓

13. UI Rendering
    ↓
    Dashboard: Metrics + Charts
    VulnerabilityList: Expandable items
    Monaco Editor: Code display
```

### Data Structures

```javascript
// Request
{
  "path": "/Users/user/project",
  "model": "llama3.1:8b"
}

// Response
{
  "project_path": "/Users/user/project",
  "issues": [
    {
      "file_path": "vulnerable.py",
      "line_number": 14,
      "column": 5,
      "rule_id": "PY-AST-002",
      "vulnerability_type": "Command Injection",
      "severity": "Critical",
      "description": "subprocess call with shell=True...",
      "confidence": "High",
      "snippet": "subprocess.call(cmd, shell=True)",
      "suggested_fix": "subprocess.call(shlex.split(cmd))",
      "fix_theory": "Use shlex.split() to safely parse..."
    }
  ],
  "smell_score": 85.5,
  "scan_duration": 2.34,
  "files_scanned": 42
}
```

---

## 8. Development Workflow

### Running the Application

**Option 1: Desktop App (Electron)**

```bash
# Terminal 1: Start Python server
cd server
source .venv/bin/activate
python main.py

# Terminal 2: Start Electron app
cd client
npm run electron:dev
```

**Option 2: Web App**

```bash
# Terminal 1: Start Python server
cd server
source .venv/bin/activate
python main.py

# Terminal 2: Start React dev server
cd client
npm run dev
# Open http://localhost:5173
```

**Option 3: CLI**

```bash
cd server
source .venv/bin/activate
python main.py scan --path /path/to/project
```

### Building for Production

**Desktop App**

```bash
cd client
npm run electron:build
# Output: client/release/
```

**Web App**

```bash
cd client
npm run build
# Output: client/dist/
```

### Development Tools

- **Backend**: Python debugger, FastAPI docs (`/docs`)
- **Frontend**: React DevTools, Vite HMR
- **Electron**: DevTools (auto-opens in dev mode)

---

## 9. Key Concepts

### 1. Static Analysis (SAST)

**What**: Analyzing source code without executing it

**How**: Parse code into Abstract Syntax Tree (AST), analyze nodes

**Example**:
```python
# Code
subprocess.call(cmd, shell=True)

# AST
Call(
  func=Attribute(value=Name(id='subprocess'), attr='call'),
  keywords=[keyword(arg='shell', value=Constant(value=True))]
)

# Detection
if keyword.arg == 'shell' and keyword.value == True:
    # Vulnerability found!
```

### 2. Taint Analysis

**What**: Tracking data flow from untrusted sources to dangerous sinks

**Concepts**:
- **Source**: User input (e.g., `request.args`)
- **Sink**: Dangerous function (e.g., `db.execute()`)
- **Taint**: Data is "tainted" if it flows from source to sink without sanitization

**Example**:
```python
# Source (tainted)
user_id = request.args.get('id')

# Sink (vulnerable if tainted)
query = f"SELECT * FROM users WHERE id = {user_id}"
db.execute(query)  # SQL Injection!
```

### 3. LLM Validation

**What**: Using AI to validate findings and reduce false positives

**Process**:
1. Format vulnerability as natural language prompt
2. Send to local LLM (Ollama)
3. Parse AI response
4. Extract validation + fix suggestion

**Benefits**:
- Reduces false positives
- Provides context-aware fixes
- Explains why vulnerability is dangerous

### 4. Smell Score

**What**: Overall code security health metric (0-100)

**Calculation**:
```
Score = Σ(severity_weight × issue_count)

Weights:
- Critical: 10
- High: 7
- Medium: 4
- Low: 2

Normalized to 0-100 scale
```

**Interpretation**:
- 0-20: Excellent
- 21-40: Good
- 41-60: Fair
- 61-80: Poor
- 81-100: Critical

### 5. Content Security Policy (CSP)

**What**: HTTP header that controls what resources can be loaded

**Purpose**: Prevent XSS, code injection, and other attacks

**Vulnora AI CSP**:
```
script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net
style-src 'self' 'unsafe-inline' https://fonts.googleapis.com
font-src 'self' data: https://fonts.gstatic.com
```

**Why**:
- `'unsafe-eval'`: Monaco Editor needs dynamic code evaluation
- `cdn.jsdelivr.net`: Monaco loads from CDN
- `data:`: Inline fonts for icons

---

## 10. File-by-File Breakdown

### Backend Files

| File | Purpose | Key Functions |
|------|---------|---------------|
| `main.py` | Entry point | `start_api()`, `main()` |
| `vulnora/api/main.py` | API routes | `POST /scan`, `GET /health` |
| `vulnora/core/scanner.py` | Scanner orchestrator | `scan()`, `discover_files()` |
| `vulnora/core/patterns.py` | Vulnerability patterns | Pattern definitions |
| `vulnora/scanners/regex.py` | Regex scanner | `scan_file()` |
| `vulnora/scanners/sast.py` | AST scanner | `analyze_ast()` |
| `vulnora/analyzers/taint.py` | Taint analyzer | `track_taint()` |
| `vulnora/llm/engine.py` | LLM client | `validate_issue()` |
| `vulnora/models/issue.py` | Data model | `Issue` class |

### Frontend Files

| File | Purpose | Key Components |
|------|---------|----------------|
| `src/main.jsx` | React entry | `ReactDOM.createRoot()` |
| `src/App.jsx` | Root component | `App` |
| `src/components/LandingPage.jsx` | Welcome screen | `LandingPage` |
| `src/components/ScanForm.jsx` | Scan input form | `ScanForm` |
| `src/components/Dashboard.jsx` | Metrics display | `Dashboard`, charts |
| `src/components/VulnerabilityList.jsx` | Issue list | `VulnerabilityList`, `VulnerabilityItem` |
| `src/context/ThemeContext.jsx` | Theme management | `ThemeProvider`, `useTheme` |
| `src/index.css` | Global styles | CSS variables, utilities |

### Electron Files

| File | Purpose | Key Functions |
|------|---------|---------------|
| `electron/main.js` | Main process | `createWindow()`, IPC handlers |
| `electron/preload.js` | Preload script | `contextBridge.exposeInMainWorld()` |

### Configuration Files

| File | Purpose |
|------|---------|
| `package.json` | NPM dependencies, scripts, Electron build config |
| `vite.config.js` | Vite build configuration, Electron plugins |
| `tailwind.config.js` | Tailwind CSS configuration |
| `requirements.txt` | Python dependencies |

---

## Summary

Vulnora AI is a sophisticated security scanner that combines:

1. **Multiple Analysis Techniques**: Regex, SAST, Taint Analysis
2. **AI Validation**: LLM reduces false positives
3. **Modern Stack**: React + FastAPI + Electron
4. **Offline Operation**: Complete privacy, no cloud uploads
5. **Rich UI**: Monaco Editor, charts, expandable details
6. **Cross-Platform**: Desktop app for macOS, Windows, Linux

**Key Strengths**:
- ✅ Comprehensive scanning (7+ languages)
- ✅ Parallel processing for speed
- ✅ AI-powered validation
- ✅ Beautiful, modern UI
- ✅ Multiple interfaces (Desktop, Web, CLI)
- ✅ Completely offline

**Study Tips**:
1. Start with `main.py` to understand entry points
2. Follow a scan request through the entire flow
3. Examine one scanner in detail (start with regex)
4. Understand the React component hierarchy
5. Explore Electron IPC communication
6. Review the data models and API contracts

This documentation covers every major aspect of Vulnora AI. Use it as a reference while exploring the codebase!
