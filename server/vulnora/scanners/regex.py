import logging
from typing import List
from vulnora.models.issue import IssueCandidate
from vulnora.core.patterns import PATTERNS

logger = logging.getLogger("vulnora.scanners.regex")

class RegexScanner:
    def scan_file(self, file_path: str, content: str) -> List[IssueCandidate]:
        issues = []
        ext = file_path.split('.')[-1]
        lang = "python" if ext == "py" else "javascript" if ext in ["js", "ts", "jsx", "tsx"] else "java" if ext == "java" else None
        
        if not lang or lang not in PATTERNS:
            return []

        lines = content.split('\n')
        for i, line in enumerate(lines):
            for pattern in PATTERNS[lang]:
                if pattern.regex.search(line):
                    issues.append(IssueCandidate(
                        file_path=file_path,
                        line_number=i + 1,
                        column=0,
                        rule_id=pattern.id,
                        vulnerability_type=pattern.name,
                        severity=pattern.severity,
                        description=pattern.description,
                        confidence="Medium",
                        snippet=line.strip(),
                        suggested_fix=pattern.fix if pattern.fix else "Review and refactor code to remove vulnerability.",
                        fix_theory=pattern.fix_theory
                    ))
        return issues
