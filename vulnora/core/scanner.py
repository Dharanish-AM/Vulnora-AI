import os
import logging
from typing import List, Set
from vulnora.models.issue import IssueCandidate
from vulnora.core.patterns import StaticScanner
from vulnora.core.taint_analysis import TaintAnalyzer
from vulnora.core.llm import LLMValidator

logger = logging.getLogger("vulnora.scanner")

class ProjectScanner:
    def __init__(self, project_path: str, llm_model: str = "llama3.1:8b"):
        self.project_path = project_path
        self.llm_validator = LLMValidator(model=llm_model) if llm_model else None
        self.supported_extensions = {'.py', '.js', '.jsx', '.ts', '.tsx', '.java'}
        self.excluded_dirs = {'.git', '.venv', 'node_modules', 'dist', 'build', '__pycache__', 'target', '.idea', '.vscode'}
        self.files_to_scan = []

    def discover_files(self) -> List[str]:
        """Recursively discover files to scan."""
        logger.info(f"Discovering files in {self.project_path}...")
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
        static_scanner = StaticScanner()
        
        logger.info("Starting static analysis...")
        for file_path in self.files_to_scan:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                # Static Scan
                static_issues = static_scanner.scan_file(file_path, content)
                if static_issues:
                    logger.debug(f"Found {len(static_issues)} static issues in {file_path}")
                for issue in static_issues:
                    issues.append(IssueCandidate(**issue))

                # Taint Analysis (Python only)
                if file_path.endswith('.py'):
                    taint_analyzer = TaintAnalyzer()
                    taint_issues = taint_analyzer.scan_file(file_path, content)
                    if taint_issues:
                        logger.debug(f"Found {len(taint_issues)} taint issues in {file_path}")
                    for issue in taint_issues:
                        issues.append(IssueCandidate(**issue))
                
                # LLM Validation (Optional: could be a separate step or flag)
                # For now, we'll just validate high severity issues to save time
                if self.llm_validator:
                    for i, issue in enumerate(issues):
                        if issue.severity in ["High", "Critical"] and issue.confidence == "Low":
                             logger.info(f"Validating issue with LLM: {issue.vulnerability_type} in {os.path.basename(issue.file_path)}")
                             issues[i] = self.llm_validator.validate_issue(issue)

            except Exception as e:
                logger.error(f"Error scanning {file_path}: {e}")
                
        return issues
