import re
from typing import List, Dict

class Pattern:
    def __init__(self, id: str, name: str, regex: str, severity: str, description: str):
        self.id = id
        self.name = name
        self.regex = re.compile(regex, re.IGNORECASE)
        self.severity = severity
        self.description = description

PATTERNS = {
    "python": [
        Pattern("PY-001", "Hardcoded Secret", r"(api_key|secret|password|token)\s*=\s*['\"][A-Za-z0-9_\-]{20,}['\"]", "High", "Hardcoded secret detected"),
        Pattern("PY-002", "SQL Injection", r"execute\s*\(\s*f?['\"].*\{.*\}.*['\"]\s*\)", "Critical", "Potential SQL Injection via f-string or format"),
        Pattern("PY-003", "Command Injection", r"(subprocess\.Popen|os\.system|os\.popen)\s*\(.*shell\s*=\s*True.*\)", "Critical", "Command injection risk with shell=True"),
        Pattern("PY-004", "Insecure Hash", r"hashlib\.md5\(", "Medium", "Use of weak hashing algorithm (MD5)"),
        Pattern("PY-005", "Debug Mode", r"debug\s*=\s*True", "Low", "Debug mode enabled in production"),
    ],
    "javascript": [
        Pattern("JS-001", "Hardcoded Secret", r"(apiKey|secret|password|token)\s*[:=]\s*['\"][A-Za-z0-9_\-]{20,}['\"]", "High", "Hardcoded secret detected"),
        Pattern("JS-002", "Eval Usage", r"eval\s*\(", "Critical", "Use of eval() is dangerous"),
        Pattern("JS-003", "Inner HTML", r"\.innerHTML\s*=", "Medium", "Potential XSS via innerHTML"),
    ],
    "java": [
        Pattern("JV-001", "Hardcoded Secret", r"(apiKey|secret|password|token)\s*=\s*['\"][A-Za-z0-9_\-]{20,}['\"]", "High", "Hardcoded secret detected"),
        Pattern("JV-002", "SQL Injection", r"Statement\s*=\s*.*execute.*\(", "Critical", "Potential SQL Injection"),
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
