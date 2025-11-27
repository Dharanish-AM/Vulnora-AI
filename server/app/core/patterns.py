import re
from typing import List, Dict

class Pattern:
    def __init__(self, id: str, name: str, regex: str, severity: str, description: str, fix: str = None, fix_theory: str = None):
        self.id = id
        self.name = name
        self.regex = re.compile(regex, re.IGNORECASE)
        self.severity = severity
        self.description = description
        self.fix = fix
        self.fix_theory = fix_theory

PATTERNS = {
    "python": [
        Pattern("PY-001", "Hardcoded Secret", r"(api_key|secret|password|token)\s*=\s*['\"][A-Za-z0-9_\-]{20,}['\"]", "High", "Hardcoded secret detected", 
                fix="import os\nsecret = os.getenv('SECRET_KEY')",
                fix_theory="Hardcoding secrets in source code is insecure as it exposes them to anyone with access to the code. Using environment variables separates configuration from code, keeping secrets safe."),
        Pattern("PY-002", "SQL Injection", r"execute\s*\(\s*f?['\"].*\{.*\}.*['\"]\s*\)", "Critical", "Potential SQL Injection via f-string or format",
                fix="cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))",
                fix_theory="Constructing SQL queries with string formatting allows attackers to manipulate the query structure. Parameterized queries ensure inputs are treated as data, not executable code."),
        Pattern("PY-003", "Command Injection", r"(subprocess\.Popen|os\.system|os\.popen)\s*\(.*shell\s*=\s*True.*\)", "Critical", "Command injection risk with shell=True",
                fix="subprocess.run(['ls', '-l'], shell=False)",
                fix_theory="Using shell=True invokes a system shell, allowing attackers to execute arbitrary commands via shell metacharacters. Setting shell=False (default) executes the command directly, preventing injection."),
        Pattern("PY-004", "Insecure Hash", r"hashlib\.md5\(", "Medium", "Use of weak hashing algorithm (MD5)",
                fix="hashlib.sha256(data).hexdigest()",
                fix_theory="MD5 is a weak hashing algorithm susceptible to collision attacks. SHA-256 provides a much higher level of security and collision resistance."),
        Pattern("PY-005", "Debug Mode", r"debug\s*=\s*True", "Low", "Debug mode enabled in production",
                fix="DEBUG = os.getenv('DEBUG', 'False') == 'True'",
                fix_theory="Running in debug mode in production can leak sensitive information like stack traces and configuration details. Use environment variables to toggle debug mode safely."),
    ],
    "javascript": [
        Pattern("JS-001", "Hardcoded Secret", r"(apiKey|secret|password|token)\s*[:=]\s*['\"][A-Za-z0-9_\-]{20,}['\"]", "High", "Hardcoded secret detected",
                fix="const apiKey = process.env.API_KEY;",
                fix_theory="Hardcoding secrets exposes them in the client-side bundle or server code. Use environment variables (process.env) to inject secrets at runtime securely."),
        Pattern("JS-002", "Eval Usage", r"eval\s*\(", "Critical", "Use of eval() is dangerous",
                fix="JSON.parse(data)",
                fix_theory="The eval() function executes a string as code, which can be exploited to run malicious code. Use safer alternatives like JSON.parse() for data or refactor logic to avoid dynamic execution."),
        Pattern("JS-003", "Inner HTML", r"\.innerHTML\s*=", "Medium", "Potential XSS via innerHTML",
                fix="element.textContent = 'Safe text';",
                fix_theory="Setting innerHTML allows the browser to parse and execute HTML/scripts, leading to XSS. Use textContent or innerText to treat input as plain text."),
    ],
    "java": [
        Pattern("JV-001", "Hardcoded Secret", r"(apiKey|secret|password|token)\s*=\s*['\"][A-Za-z0-9_\-]{20,}['\"]", "High", "Hardcoded secret detected",
                fix="String apiKey = System.getenv(\"API_KEY\");",
                fix_theory="Hardcoded secrets can be easily extracted from compiled bytecode. Use System.getenv() to retrieve secrets from the environment at runtime."),
        Pattern("JV-002", "SQL Injection", r"Statement\s*=\s*.*execute.*\(", "Critical", "Potential SQL Injection",
                fix="PreparedStatement stmt = conn.prepareStatement(\"SELECT * FROM users WHERE id = ?\");",
                fix_theory="Concatenating strings to build SQL queries is vulnerable to injection. PreparedStatement uses placeholders (?) to safely bind parameters, preventing malicious SQL execution."),
    ]
}

class StaticScanner:
    def scan_file(self, file_path: str, content: str) -> List[Dict]:
        issues = []
        ext = file_path.split('.')[-1]
        lang = "python" if ext == "py" else "javascript" if ext in ["js", "ts", "jsx", "tsx"] else "java" if ext == "java" else None
        
        if not lang or lang not in PATTERNS:
            return []

        lines = content.split('\n')
        for i, line in enumerate(lines):
            for pattern in PATTERNS[lang]:
                if pattern.regex.search(line):
                    issues.append({
                        "file_path": file_path,
                        "line_number": i + 1,
                        "column": 0, # Regex doesn't easily give column without more work
                        "rule_id": pattern.id,
                        "vulnerability_type": pattern.name,
                        "severity": pattern.severity,
                        "description": pattern.description,
                        "snippet": line.strip(),
                        "suggested_fix": "Review and refactor code to remove vulnerability."
                    })
        return issues
