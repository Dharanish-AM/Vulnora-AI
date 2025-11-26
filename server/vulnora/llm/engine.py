import os
import logging
from typing import Optional, Dict
from vulnora.models.issue import IssueCandidate

logger = logging.getLogger("vulnora.llm.engine")

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
