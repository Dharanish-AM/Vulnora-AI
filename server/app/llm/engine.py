import os
import re
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
                    "num_predict": 4096
                }
            }
            response = requests.post(self.api_url, json=payload, timeout=120)
            response.raise_for_status()
            return response.json().get("response", "").strip()
        except Exception as e:
            logger.error(f"Ollama API call failed: {e}")
            return ""

    def _clean_json_response(self, response: str) -> str:
        """
        Clean up the LLM response to ensure it's valid JSON.
        Handles markdown code blocks, conversational text, and invalid escape sequences.
        """
        if not response:
            return ""
            
        # Try to extract JSON from markdown code blocks
        code_block_pattern = r"```(?:json)?\s*(.*?)```"
        match = re.search(code_block_pattern, response, re.DOTALL)
        if match:
            clean_response = match.group(1).strip()
        else:
            # If no code block, try to find the first [ and last ]
            start = response.find('[')
            end = response.rfind(']')
            if start != -1 and end != -1 and end > start:
                clean_response = response[start:end+1]
            else:
                clean_response = response.strip()
        
        # Fix invalid escape sequences
        # This regex matches valid escapes: \", \\, \/, \b, \f, \n, \r, \t, \uXXXX
        # It captures valid escapes in group 1, and invalid backslashes in group 2
        pattern = r'(\\(?:["\\/bfnrt]|u[0-9a-fA-F]{4}))|(\\)'
        
        def replace_match(match):
            if match.group(1):
                return match.group(1)
            return "\\\\"
            
        return re.sub(pattern, replace_match, clean_response)

    def scan_file(self, file_path: str, content: str) -> list[IssueCandidate]:
        """
        Scan a file for vulnerabilities using the LLM.
        """
        prompt = f"""Analyze this code for security vulnerabilities.
File: {file_path}

Code:
```
{content}
```

Instructions:
1. Identify security issues (OWASP Top 10, CWE Top 25, Secrets, Logic Bugs).
2. Be concise. Focus on high-confidence issues.
3. Return a JSON array.

Format:
[
    {{
        "type": "Vulnerability Type",
        "severity": "Critical/High/Medium/Low",
        "line": <line_number>,
        "description": "Brief explanation of the risk.",
        "vulnerable_code": "The exact code snippet.",
        "fix_theory": "Brief explanation of the fix.",
        "fixed_code": "Secure code snippet."
    }}
]

Return [] if no issues found.
"""
        
        logger.info(f"🤖 Analyzing {file_path} with {self.provider}...")
        logger.debug(f"Prompt sent to LLM:\n{prompt[:500]}...") # Log truncated prompt
        
        response = self._call_ollama(prompt)
        
        logger.debug(f"📝 Raw LLM Response for {file_path}:\n{response}")
        issues = []
        
        if not response:
            return issues

        try:
            # Clean up response
            clean_response = self._clean_json_response(response)
            
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
                
                logger.info(f"✅ Successfully parsed {len(issues)} issues from {file_path}")
                    
        except json.JSONDecodeError as e:
            logger.error(f"❌ Failed to parse LLM response for {file_path}: {e}")
            logger.error(f"Malformed JSON Content:\n{response}")
        except Exception as e:
            logger.error(f"Error processing LLM response for {file_path}: {e}")
            
        return issues

    def analyze_issue(self, issue: IssueCandidate) -> IssueCandidate:
        """
        Analyze an issue to verify it and provide a better description/fix.
        """
        prompt = f"""Verify this vulnerability.
Type: {issue.vulnerability_type}
Code:
```
{issue.snippet}
```

Task:
1. Determine if REAL or FALSE_POSITIVE.
2. Explain briefly.

Format:
VERDICT: [REAL/FALSE_POSITIVE]
EXPLANATION: [Brief explanation]
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
    
    def _clean_code_response(self, response: str) -> str:
        """
        Clean up the LLM response to ensure it's valid code.
        Handles markdown code blocks.
        """
        if not response:
            return ""
            
        # Try to extract code from markdown code blocks
        code_block_pattern = r"```(?:\w+)?\s*(.*?)```"
        match = re.search(code_block_pattern, response, re.DOTALL)
        if match:
            return match.group(1).strip()
            
        return response.strip()

    def generate_patch(self, issue: IssueCandidate) -> str:
        """
        Generate a code patch for the issue.
        """
        prompt = f"""You are a security expert. Provide a secure code fix for the following vulnerability.
Return ONLY the fixed code snippet. Do not include markdown formatting or explanations.
Ensure the code is complete and syntactically correct for the file type.

File: {issue.file_path}
Vulnerability: {issue.vulnerability_type}
Vulnerable Code:
{issue.snippet}

Fixed Code:
"""
        response = self._call_ollama(prompt)
        return self._clean_code_response(response)
