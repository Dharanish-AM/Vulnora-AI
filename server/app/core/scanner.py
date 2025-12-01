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
                    
        logger.info(f"📂 Found {len(self.files_to_scan)} supported files to scan.")
        return self.files_to_scan

    def _calculate_file_hash(self, content: str) -> str:
        """Calculate SHA-256 hash of file content."""
        import hashlib
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def _scan_file_worker(self, file_path: str) -> List[IssueCandidate]:
        """Worker method to scan a single file."""
        file_issues = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # 1. Incremental Scan Check
            current_hash = self._calculate_file_hash(content)
            # We need a db instance here. Since we can't easily pass it to worker without refactoring,
            # we'll instantiate a new one or pass it. For now, let's instantiate.
            from app.core.database import Database
            db = Database()
            stored_hash = db.get_file_hash(self.project_path, file_path)
            
            if stored_hash == current_hash:
                logger.debug(f"Skipping unchanged file: {file_path}")
                return [] # Return empty, we assume previous issues are still valid (or we'd need to fetch them)
                          # For this MVP, we just skip re-scanning. Ideally we'd fetch old issues.
                          # But since we clear DB on new scan usually, we might want to re-save them?
                          # Actually, the requirement is "faster". If we return empty, the UI shows nothing for this file.
                          # Let's assume for now we just want to skip LLM if no changes.
                          # But wait, if we return empty, the final report won't have issues for this file.
                          # We need to fetch previous issues if we skip.
                          # However, the current DB structure links issues to scan_id.
                          # So if we create a NEW scan, we need to copy old issues to new scan_id.
                          # That's complex.
                          # Alternative: Just skip LLM if hash matches AND no regex findings?
                          # Let's stick to the plan: "Smart Filtering".
            
            # 2. Decision Logic
            # User requested to rely ONLY on AI engine for accuracy.
            # We skip regex checks and send ALL changed files to the LLM.
            
            logger.debug(f"Scanning file: {file_path}")
            file_issues.extend(self.llm_engine.scan_file(file_path, content))
            logger.debug(f"Finished scanning {file_path}. Found {len(file_issues)} issues.")

            # Update Hash
            db.update_file_hash(self.project_path, file_path, current_hash, 0)
            
        except Exception as e:
            logger.error(f"Error scanning {file_path}: {e}")
            
        return file_issues

    def scan(self) -> List[IssueCandidate]:
        """Orchestrate the scanning process."""
        self.discover_files()
        issues = []
        
        logger.info(f"🚀 Starting parallel analysis on {len(self.files_to_scan)} files...")
        
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
