import requests
import json
import logging
from typing import Dict, Any, Optional
from vulnora.models.issue import IssueCandidate

logger = logging.getLogger("vulnora.llm")

class LLMValidator:
    def __init__(self, model: str = "llama3.1:8b", host: str = "http://localhost:11434"):
        self.model = model
        self.host = host
        self.api_url = f"{host}/api/generate"

    def validate_issue(self, issue: IssueCandidate) -> IssueCandidate:
        """
        Send the issue to LLM for validation and detailed analysis.
        """
        prompt = self._create_prompt(issue)
        
        try:
            response = requests.post(self.api_url, json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "format": "json"
            })
            
            if response.status_code == 200:
                result = response.json()
                analysis = json.loads(result.get("response", "{}"))
                
                logger.debug(f"LLM Response: {analysis}")

                # Update issue with LLM insights
                if analysis.get("confidence"):
                    issue.confidence = analysis["confidence"]
                if analysis.get("severity"):
                    issue.severity = analysis["severity"]
                if analysis.get("description"):
                    issue.description = analysis["description"]
                if analysis.get("suggested_fix"):
                    issue.suggested_fix = analysis["suggested_fix"]
            else:
                logger.error(f"LLM API Error: {response.status_code} - {response.text}")
                    
        except Exception as e:
            logger.error(f"LLM Validation failed: {e}")
            
        return issue

    def _create_prompt(self, issue: IssueCandidate) -> str:
        return f"""
        You are a security expert. Analyze the following code snippet for vulnerabilities.
        
        Vulnerability Type: {issue.vulnerability_type}
        File: {issue.file_path}
        Line: {issue.line_number}
        Snippet:
        ```
        {issue.snippet}
        ```
        
        Respond in JSON format with the following keys:
        - confidence: (High, Medium, Low) - How sure are you this is a real vulnerability?
        - severity: (Critical, High, Medium, Low) - How severe is this?
        - description: A brief explanation of why this is a vulnerability.
        - suggested_fix: A code snippet or description of how to fix it.
        
        If it is a false positive, set confidence to "Low" and explain why.
        """
