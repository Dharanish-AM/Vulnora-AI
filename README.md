# 🛡️ Vulnora AI

**AI-Powered Multi-Language Code Security Scanner**

Vulnora AI is an advanced, offline security scanner designed to analyze software projects for vulnerabilities using a combination of static analysis, AST-based taint detection, and local Large Language Models (LLMs). It provides detailed vulnerability reports, suggested fixes, and a visual dashboard—all without your code ever leaving your machine.

---

## 🚀 Key Features

-   **Multi-Language Support**: Scans Python, JavaScript, TypeScript, and Java projects.
-   **Hybrid Analysis Engine**:
    -   **Static Pattern Matching**: Detects known vulnerability patterns (regex/heuristics).
    -   **AST Taint Analysis**: Tracks dangerous data flows (e.g., user input → `eval` or `subprocess`) in Python.
    -   **LLM Validation**: Uses local LLMs (via Ollama) to validate findings, reduce false positives, and provide context-aware fixes.
-   **Offline & Private**: Runs entirely on your local machine. No code is uploaded to the cloud.
-   **Interactive Dashboard**: Streamlit-based UI for easy scanning and result visualization.
-   **REST API**: FastAPI backend for integration into CI/CD pipelines or other tools.
-   **Smart Scoring**: Calculates a "Smell Score" to gauge the overall security health of your project.
-   **Smart Scoring**: Calculates a "Smell Score" to gauge the overall security health of your project.
-   **Modern React UI**: A sleek, dark-mode enabled React client built with Vite and TailwindCSS.
-   **Comprehensive Logging**: Detailed server-side logs for debugging and audit trails.
---

## 🛠️ Architecture

Vulnora AI consists of modular components:

-   **Scanner Engine**: Recursively discovers files and orchestrates analysis.
-   **Taint Analyzer**: Python AST visitor that tracks tainted variables to dangerous sinks.
-   **LLM Reasoner**: Connects to a local Ollama instance to analyze code snippets.
-   **FastAPI Backend**: Exposes scanning capabilities via a RESTful API.
-   **Streamlit Dashboard**: Provides a user-friendly interface for developers.

---

## 📋 Prerequisites

-   **Python 3.10+**
-   **Ollama**: Required for LLM capabilities.
    -   Install Ollama: [https://ollama.com/](https://ollama.com/)
    -   Pull the default model: `ollama pull llama3.1:8b` (or `llama3`, `mistral`)

---

## 📦 Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/Vulnora-AI.git
    cd Vulnora-AI
    ```

2.  **Create a virtual environment**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

---

## 🚦 Usage

Vulnora AI runs as two separate processes: the Backend API and the Dashboard.

### 1. Start the Backend API
The API handles the heavy lifting of scanning and analysis.
```bash
python main.py api
```
*Server starts at `http://0.0.0.0:8000`*

### 2. Start the Dashboard (Streamlit)
The Dashboard provides the visual interface. Open a new terminal:
```bash
source .venv/bin/activate
python main.py dashboard
```
*Dashboard opens at `http://localhost:8501`*

### 3. Start the React Client (Alternative UI)
For a more modern experience, use the React client:
```bash
cd client
npm install
npm run dev
```
*Client opens at `http://localhost:5173`*

### 4. Run a Scan
1.  Open the Dashboard (Streamlit or React) in your browser.

2.  Enter the **absolute path** to the project you want to scan.
3.  Select your desired LLM model.
4.  Click **Start Scan**.

---

## 📂 Project Structure

```
Vulnora-AI/
├── main.py              # Entry point for API and Dashboard
├── requirements.txt     # Python dependencies
├── vulnora/
│   ├── api/             # FastAPI application
│   ├── core/            # Core logic (Scanner, Taint Analysis, LLM)
│   ├── dashboard/       # Streamlit UI
│   ├── models/          # Pydantic data models
│   └── utils/           # Helper functions
├── client/              # React + Vite Frontend
│   ├── src/             # React source code
│   └── vite.config.js   # Vite configuration
└── test_project/        # Sample vulnerable project for testing
```

---

## 🧪 Testing

A `test_project` is included to verify the scanner's capabilities. It contains:
-   `vulnerable.py`: Contains Command Injection, Hardcoded Secrets, and Taint Flow issues.
-   `vulnerable.js`: Contains Hardcoded Secrets, Eval Usage, and XSS vulnerabilities.

Scan this directory to see Vulnora AI in action!

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
