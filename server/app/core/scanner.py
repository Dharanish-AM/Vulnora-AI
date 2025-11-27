import os
import logging
import concurrent.futures
from typing import List
from app.models.issue import IssueCandidate
from app.llm.engine import LLMEngine

logger = logging.getLogger("app.scanner")

class ProjectScanner:
    def __init__(self, project_path: str, llm_model: str = "gemini"):
        self.project_path = project_path
        self.llm_engine = LLMEngine(provider=llm_model)
        self.supported_extensions = {'.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.go', '.rs', '.cpp', '.c', '.h'}
        self.excluded_dirs = {
            '.git', '.venv', 'venv', 'env', 'node_modules', 'dist', 'build', 
            '__pycache__', 'target', '.idea', '.vscode', '.tox', 'coverage', 
            'tmp', 'temp', 'logs', 'vendor', 'bin', 'obj', '.next', '.nuxt'
        }
        self.files_to_scan = []
        
        # Initialize scanners
        # self.regex_scanner = RegexScanner()
        # self.sast_scanner = SASTScanner()
        # self.taint_analyzer = TaintAnalyzer()

    def discover_files(self) -> List[str]:
        """Recursively discover files to scan."""
        logger.info(f"Discovering files in {self.project_path}...")
        self.files_to_scan = []
        
        # Normalize excluded dirs for case-insensitive comparison
        excluded_dirs_lower = {d.lower() for d in self.excluded_dirs}
        
        for root, dirs, files in os.walk(self.project_path):
            # Modify dirs in-place to skip excluded directories
            # We iterate over a copy of dirs to safely modify the original list
            original_dirs = list(dirs)
            dirs[:] = []
            for d in original_dirs:
                if d.lower() not in excluded_dirs_lower:
                    dirs.append(d)
                else:
                    logger.debug(f"Skipping excluded directory: {os.path.join(root, d)}")
            
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in self.supported_extensions:
                    self.files_to_scan.append(os.path.join(root, file))
                    
        logger.info(f"Found {len(self.files_to_scan)} files to scan.")
        return self.files_to_scan

    def _scan_file_worker(self, file_path: str) -> List[IssueCandidate]:
        """Worker method to scan a single file."""
        file_issues = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            # LLM Scan
            file_issues.extend(self.llm_engine.scan_file(file_path, content))
            
        except Exception as e:
            logger.error(f"Error scanning {file_path}: {e}")
            
        return file_issues

    def scan(self) -> List[IssueCandidate]:
        """Orchestrate the scanning process."""
        self.discover_files()
        issues = []
        
        logger.info(f"Starting parallel analysis on {len(self.files_to_scan)} files...")
        
        # Use ThreadPoolExecutor for parallel scanning
        # Adjust max_workers based on CPU cores or I/O bound nature
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_file = {executor.submit(self._scan_file_worker, fp): fp for fp in self.files_to_scan}
            
            for future in concurrent.futures.as_completed(future_to_file):
                try:
                    file_issues = future.result()
                    issues.extend(file_issues)
                except Exception as e:
                    logger.error(f"File scan generated an exception: {e}")

        # Deduplication is handled by LLM response structure implicitly (or we can add simple one)
        # For now, just return issues
        return issues

    # def _deduplicate_issues(self, issues: List[IssueCandidate]) -> List[IssueCandidate]:
    #     """
    #     Deduplicate issues based on file path and line number.
    #     Prioritize SAST/Taint issues over Regex issues.
    #     """
    #     unique_issues = {}
    #     
    #     for issue in issues:
    #         key = (issue.file_path, issue.line_number)
    #         
    #         if key not in unique_issues:
    #             unique_issues[key] = issue
    #         else:
    #             existing = unique_issues[key]
    #             # If existing is Regex (starts with PY- or JS- or JV-) and new is SAST (starts with PY-AST- or PY-TAINT-), replace it
    #             # Or if new has higher confidence
    #             
    #             is_existing_sast = "AST" in existing.rule_id or "TAINT" in existing.rule_id
    #             is_new_sast = "AST" in issue.rule_id or "TAINT" in issue.rule_id
    #             
    #             if not is_existing_sast and is_new_sast:
    #                 unique_issues[key] = issue
    #             elif is_existing_sast and not is_new_sast:
    #                 continue # Keep existing SAST
    #             else:
    #                 # Both are same type, keep the one with higher severity or just first one
    #                 pass
    #                 
    #     return list(unique_issues.values())
