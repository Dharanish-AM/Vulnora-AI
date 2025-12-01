from pydantic import BaseModel
from typing import Optional, List

class IssueCandidate(BaseModel):
    file_path: str
    line_number: int
    column: int
    rule_id: str
    vulnerability_type: str
    severity: str
    description: str
    confidence: str = "Low"
    snippet: Optional[str] = None
    suggested_fix: Optional[str] = None
    fix_theory: Optional[str] = None

class ScanResult(BaseModel):
    scan_id: Optional[int] = None
    project_path: str
    issues: List[IssueCandidate]
    smell_score: float = 0.0
    scan_duration: float = 0.0
    files_scanned: int = 0
