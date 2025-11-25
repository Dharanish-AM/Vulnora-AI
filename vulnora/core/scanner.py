import os
from typing import List, Set
from vulnora.models.issue import IssueCandidate
from vulnora.core.patterns import StaticScanner
from vulnora.core.taint_analysis import TaintAnalyzer
from vulnora.core.llm import LLMValidator

class ProjectScanner:
    def __init__(self, project_path: str, llm_model: str = "llama3.1:8b"):
        self.project_path = project_path
        self.llm_validator = LLMValidator(model=llm_model) if llm_model else None
        self.supported_extensions = {'.py', '.js', '.jsx', '.ts', '.tsx', '.java'}
        self.excluded_dirs = {'.git', '.venv', 'node_modules', 'dist', 'build', '__pycache__'}
        self.files_to_scan = []

    def discover_files(self) -> List[str]:
        """Recursively discover files to scan."""
        for root, dirs, files in os.walk(self.project_path):
            # Modify dirs in-place to skip excluded directories
            dirs[:] = [d for d in dirs if d not in self.excluded_dirs]
            
            for file in files:
                ext = os.path.splitext(file)[1]
                if ext in self.supported_extensions:
                    self.files_to_scan.append(os.path.join(root, file))
        return self.files_to_scan

    def scan(self) -> List[IssueCandidate]:
        """Orchestrate the scanning process."""
        self.discover_files()
        issues = []
        static_scanner = StaticScanner()
        
        for file_path in self.files_to_scan:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                # Static Scan
                static_issues = static_scanner.scan_file(file_path, content)
                for issue in static_issues:
                    issues.append(IssueCandidate(**issue))

                # Taint Analysis (Python only)
                if file_path.endswith('.py'):
                    taint_analyzer = TaintAnalyzer()
                    taint_issues = taint_analyzer.scan_file(file_path, content)
                    for issue in taint_issues:
                        issues.append(IssueCandidate(**issue))
                
                # LLM Validation (Optional: could be a separate step or flag)
                # For now, we'll just validate high severity issues to save time
                if self.llm_validator:
                    for i, issue in enumerate(issues):
                        if issue.severity in ["High", "Critical"] and issue.confidence == "Low":
                             issues[i] = self.llm_validator.validate_issue(issue)

            except Exception as e:
                print(f"Error scanning {file_path}: {e}")
                
        return issues
