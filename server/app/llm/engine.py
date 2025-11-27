import os
import logging
from typing import Optional, Dict
from app.models.issue import IssueCandidate

logger = logging.getLogger("app.llm.engine")

import requests
import json

class LLMEngine:
    def __init__(self, provider: str = "llama3.1:8b", api_key: Optional[str] = None):
        self.provider = provider
        self.api_url = "http://localhost:11434/api/generate"

    def _call_ollama(self, prompt: str) -> str:
        try:
            payload = {
                "model": self.provider,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.2,
                    "num_predict": 512
                }
            }
            response = requests.post(self.api_url, json=payload, timeout=30)
            response.raise_for_status()
            return response.json().get("response", "").strip()
        except Exception as e:
            logger.error(f"Ollama API call failed: {e}")
            return ""

    def scan_file(self, file_path: str, content: str) -> list[IssueCandidate]:
        """
        Scan a file for vulnerabilities using the LLM.
        """
        prompt = f"""You are a senior security engineer. Analyze the following code for security vulnerabilities.
File: {file_path}

Code:
```
{content}
```

Instructions:
1. Identify potential security vulnerabilities (OWASP Top 10, etc.).
2. Ignore minor style issues or best practices unless they have security implications.
3. For each vulnerability found, provide:
   - Type (e.g., SQL Injection, XSS)
   - Severity (Critical, High, Medium, Low)
   - Line Number (approximate)
   - Description (concise)
   - Vulnerable Code (exact snippet from the file)
   - Fix Theory (explanation of why the fix works)
   - Fixed Code (secure code snippet to replace the vulnerable code)

Format your response as a JSON array of objects. Do NOT include any text outside the JSON.
Example format:
[
    {{
        "type": "SQL Injection",
        "severity": "High",
        "line": 10,
        "description": "User input concatenated directly into SQL query.",
        "vulnerable_code": "query = 'SELECT * FROM users WHERE name = ' + user_input",
        "fix_theory": "Using parameterized queries prevents the database from interpreting user input as SQL commands.",
        "fixed_code": "cursor.execute('SELECT * FROM users WHERE name = ?', (user_input,))"
    }}
]

If no vulnerabilities are found, return an empty array: []
"""
        
        response = self._call_ollama(prompt)
        issues = []
        
        if not response:
            return issues

        try:
            # Clean up response if it contains markdown code blocks
            clean_response = response.strip()
            if clean_response.startswith("```json"):
                clean_response = clean_response[7:]
            if clean_response.startswith("```"):
                clean_response = clean_response[3:]
            if clean_response.endswith("```"):
                clean_response = clean_response[:-3]
            
            data = json.loads(clean_response)
            
            if isinstance(data, list):
                for item in data:
                    issues.append(IssueCandidate(
                        file_path=file_path,
                        line_number=int(item.get("line", 0)),
                        column=0,
                        rule_id=f"LLM-{item.get('type', 'Unknown').replace(' ', '-')}",
                        description=item.get("description", "Detected by LLM"),
                        severity=item.get("severity", "Medium"),
                        vulnerability_type=item.get("type", "Unknown"),
                        snippet=item.get("vulnerable_code", ""),
                        fix_theory=item.get("fix_theory", ""),
                        suggested_fix=item.get("fixed_code", "")
                    ))
                    
        except json.JSONDecodeError:
            logger.error(f"Failed to parse LLM response for {file_path}: {response[:100]}...")
        except Exception as e:
            logger.error(f"Error processing LLM response for {file_path}: {e}")
            
        return issues

    def analyze_issue(self, issue: IssueCandidate) -> IssueCandidate:
        """
        Analyze an issue to verify it and provide a better description/fix.
        """
        prompt = f"""You are a senior security engineer. Analyze this potential vulnerability.

Vulnerability Type: {issue.vulnerability_type}
File: {issue.file_path}
Code Snippet:
```
{issue.snippet}
```

Task:
1. Verify if this is a real vulnerability or a false positive.
2. If real, explain WHY it is dangerous in 1 short sentence.
3. If false positive, explain why.

Format:
VERDICT: [REAL/FALSE_POSITIVE]
EXPLANATION: [Your explanation]
"""
        
        response = self._call_ollama(prompt)
        if response:
            if "VERDICT: FALSE_POSITIVE" in response.upper():
                issue.confidence = "Low"
                issue.description = f"[AI Verified: False Positive] {response.split('EXPLANATION:', 1)[-1].strip()}"
            elif "VERDICT: REAL" in response.upper():
                issue.confidence = "High"
                explanation = response.split('EXPLANATION:', 1)[-1].strip()
                if explanation:
                    issue.description = f"{issue.description} [AI Analysis: {explanation}]"
        
        return issue

    def generate_patch(self, issue: IssueCandidate) -> str:
        """
        Generate a code patch for the issue.
        """
        prompt = f"""You are a security expert. Provide a secure code fix for the following vulnerability.
Return ONLY the fixed code snippet. Do not include markdown formatting or explanations.

Vulnerability: {issue.vulnerability_type}
Vulnerable Code:
{issue.snippet}

Fixed Code:
"""
        return self._call_ollama(prompt)
