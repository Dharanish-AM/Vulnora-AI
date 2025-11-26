import os
import logging
from typing import List
from vulnora.models.issue import IssueCandidate
from vulnora.scanners.regex import RegexScanner
from vulnora.scanners.sast import SASTScanner
from vulnora.analyzers.taint import TaintAnalyzer
from vulnora.llm.engine import LLMEngine

logger = logging.getLogger("vulnora.scanner")

class ProjectScanner:
    def __init__(self, project_path: str, llm_model: str = "gemini"):
        self.project_path = project_path
        self.llm_engine = LLMEngine(provider=llm_model)
        self.supported_extensions = {'.py', '.js', '.jsx', '.ts', '.tsx', '.java'}
        self.excluded_dirs = {'.git', '.venv', 'node_modules', 'dist', 'build', '__pycache__', 'target', '.idea', '.vscode'}
        self.files_to_scan = []
        
        # Initialize scanners
        self.regex_scanner = RegexScanner()
        self.sast_scanner = SASTScanner()
        self.taint_analyzer = TaintAnalyzer()

    def discover_files(self) -> List[str]:
        """Recursively discover files to scan."""
        logger.info(f"Discovering files in {self.project_path}...")
        self.files_to_scan = []
        for root, dirs, files in os.walk(self.project_path):
            # Modify dirs in-place to skip excluded directories
            dirs[:] = [d for d in dirs if d not in self.excluded_dirs]
            
            for file in files:
                ext = os.path.splitext(file)[1]
                if ext in self.supported_extensions:
                    self.files_to_scan.append(os.path.join(root, file))
        logger.info(f"Found {len(self.files_to_scan)} files to scan.")
        return self.files_to_scan

    def scan(self) -> List[IssueCandidate]:
        """Orchestrate the scanning process."""
        self.discover_files()
        issues = []
        
        logger.info("Starting analysis...")
        for file_path in self.files_to_scan:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                # 1. Regex Scan (Fast, covers multiple langs)
                regex_issues = self.regex_scanner.scan_file(file_path, content)
                issues.extend(regex_issues)

                # 2. SAST Scan (Python only for now)
                sast_issues = self.sast_scanner.scan_file(file_path, content)
                issues.extend(sast_issues)

                # 3. Taint Analysis (Python only)
                taint_issues = self.taint_analyzer.scan_file(file_path, content)
                issues.extend(taint_issues)
                
                # 4. Deduplicate Issues
                issues = self._deduplicate_issues(issues)

                # 5. LLM Verification (Optional/Selective)
                # For high severity issues, we can ask LLM to verify
                for issue in issues:
                    if issue.severity == "Critical" and issue.confidence != "High":
                        self.llm_engine.analyze_issue(issue)

            except Exception as e:
                logger.error(f"Error scanning {file_path}: {e}")
                
        return issues

    def _deduplicate_issues(self, issues: List[IssueCandidate]) -> List[IssueCandidate]:
        """
        Deduplicate issues based on file path and line number.
        Prioritize SAST/Taint issues over Regex issues.
        """
        unique_issues = {}
        
        for issue in issues:
            key = (issue.file_path, issue.line_number)
            
            if key not in unique_issues:
                unique_issues[key] = issue
            else:
                existing = unique_issues[key]
                # If existing is Regex (starts with PY- or JS- or JV-) and new is SAST (starts with PY-AST- or PY-TAINT-), replace it
                # Or if new has higher confidence
                
                is_existing_sast = "AST" in existing.rule_id or "TAINT" in existing.rule_id
                is_new_sast = "AST" in issue.rule_id or "TAINT" in issue.rule_id
                
                if not is_existing_sast and is_new_sast:
                    unique_issues[key] = issue
                elif is_existing_sast and not is_new_sast:
                    continue # Keep existing SAST
                else:
                    # Both are same type, keep the one with higher severity or just first one
                    pass
                    
        return list(unique_issues.values())
