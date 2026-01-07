import re
import logging
from typing import List, Dict, Tuple
from dataclasses import dataclass

logger = logging.getLogger("app.static_analyzer")

@dataclass
class StaticPattern:
    """Pattern for static vulnerability detection"""
    pattern: str
    vuln_type: str
    severity: str
    cwe_id: str

class StaticAnalyzer:
    """Fast regex-based pre-filtering for vulnerability detection"""
    
    PATTERNS: Dict[str, List[StaticPattern]] = {
        'python': [
            StaticPattern(
                r'os\.system\s*\([^)]*[\+\%f]',
                'Command Injection',
                'Critical',
                'CWE-78'
            ),
            StaticPattern(
                r'subprocess\.(call|run|Popen)\s*\([^)]*shell\s*=\s*True',
                'Command Injection via Shell',
                'Critical',
                'CWE-78'
            ),
            StaticPattern(
                r'\beval\s*\(',
                'Code Injection',
                'Critical',
                'CWE-94'
            ),
            StaticPattern(
                r'\bexec\s*\(',
                'Code Execution',
                'Critical',
                'CWE-94'
            ),
            StaticPattern(
                r'pickle\.(loads?|dumps?)\s*\(',
                'Insecure Deserialization',
                'High',
                'CWE-502'
            ),
            StaticPattern(
                r'(password|api_key|secret|token|api_secret|private_key)\s*=\s*["\'][^"\']{8,}["\']',
                'Hardcoded Credentials',
                'High',
                'CWE-798'
            ),
            StaticPattern(
                r'(sql|query)\s*=\s*["\'].*%s.*["\']|\.format\s*\(',
                'SQL Injection Risk',
                'High',
                'CWE-89'
            ),
            StaticPattern(
                r'__import__\s*\(',
                'Dynamic Import',
                'Medium',
                'CWE-94'
            ),
            StaticPattern(
                r'open\s*\([^)]*[\+\%]',
                'Path Traversal Risk',
                'High',
                'CWE-22'
            ),
            StaticPattern(
                r'\.yaml\.load\s*\([^,)]*\)',
                'Unsafe YAML Deserialization',
                'High',
                'CWE-502'
            ),
        ],
        'javascript': [
            StaticPattern(
                r'\beval\s*\(',
                'Code Injection',
                'Critical',
                'CWE-94'
            ),
            StaticPattern(
                r'innerHTML\s*=',
                'XSS Risk',
                'High',
                'CWE-79'
            ),
            StaticPattern(
                r'dangerouslySetInnerHTML',
                'React XSS Risk',
                'High',
                'CWE-79'
            ),
            StaticPattern(
                r'document\.write\s*\(',
                'DOM XSS',
                'Medium',
                'CWE-79'
            ),
            StaticPattern(
                r'(password|apiKey|secret|token|api_key)\s*[:=]\s*["\'][^"\']{8,}["\']',
                'Hardcoded Credentials',
                'High',
                'CWE-798'
            ),
            StaticPattern(
                r'new\s+Function\s*\(',
                'Dynamic Code Execution',
                'High',
                'CWE-94'
            ),
            StaticPattern(
                r'setTimeout\s*\(\s*["\']',
                'Code Injection via setTimeout',
                'Medium',
                'CWE-94'
            ),
        ],
        'typescript': [
            StaticPattern(
                r'\beval\s*\(',
                'Code Injection',
                'Critical',
                'CWE-94'
            ),
            StaticPattern(
                r'innerHTML\s*=',
                'XSS Risk',
                'High',
                'CWE-79'
            ),
            StaticPattern(
                r'dangerouslySetInnerHTML',
                'React XSS Risk',
                'High',
                'CWE-79'
            ),
            StaticPattern(
                r'(password|apiKey|secret|token|api_key)\s*[:=]\s*["\'][^"\']{8,}["\']',
                'Hardcoded Credentials',
                'High',
                'CWE-798'
            ),
        ],
        'java': [
            StaticPattern(
                r'Runtime\.getRuntime\(\)\.exec\s*\(',
                'Command Injection Risk',
                'Critical',
                'CWE-78'
            ),
            StaticPattern(
                r'Statement\.execute\s*\([^)]*\+',
                'SQL Injection',
                'Critical',
                'CWE-89'
            ),
            StaticPattern(
                r'(password|apiKey|secret)\s*=\s*"[^"]{8,}"',
                'Hardcoded Credentials',
                'High',
                'CWE-798'
            ),
        ],
    }
    
    def __init__(self):
        self.compiled_patterns: Dict[str, List[Tuple]] = {}
        self._compile_patterns()
    
    def _compile_patterns(self):
        """Pre-compile regex patterns for performance"""
        for lang, patterns in self.PATTERNS.items():
            self.compiled_patterns[lang] = [
                (re.compile(p.pattern), p.vuln_type, p.severity, p.cwe_id)
                for p in patterns
            ]
        logger.info(f"✅ Compiled {sum(len(p) for p in self.compiled_patterns.values())} static patterns")
    
    def detect_language(self, file_path: str) -> str:
        """Detect programming language from file extension"""
        ext_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.ts': 'typescript',
            '.tsx': 'typescript',
            '.java': 'java',
            '.go': 'go',
            '.rs': 'rust',
            '.cpp': 'cpp',
            '.c': 'c',
        }
        ext = file_path[file_path.rfind('.'):] if '.' in file_path else ''
        return ext_map.get(ext.lower(), 'unknown')
    
    def quick_scan(self, file_path: str, content: str) -> List[Dict]:
        """
        Fast pattern matching - returns suspicious lines.
        Returns: List of findings with line numbers and vulnerability info
        """
        lang = self.detect_language(file_path)
        if lang not in self.compiled_patterns:
            return []
        
        findings = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # Skip comments
            stripped = line.strip()
            if stripped.startswith('#') or stripped.startswith('//') or stripped.startswith('/*'):
                continue
            
            # Skip empty lines
            if not stripped:
                continue
            
            for pattern, vuln_type, severity, cwe_id in self.compiled_patterns[lang]:
                if pattern.search(line):
                    findings.append({
                        'line': line_num,
                        'type': vuln_type,
                        'severity': severity,
                        'cwe': cwe_id,
                        'snippet': line.strip()[:100],  # Limit snippet length
                        'needs_llm': True
                    })
        
        return findings
    
    def should_scan_with_llm(self, findings: List[Dict]) -> bool:
        """
        Decide if LLM scan is needed based on static findings.
        Always validate Critical/High severity findings with LLM.
        """
        if not findings:
            return False
        
        # Count Critical/High severity findings
        critical_high = [f for f in findings if f['severity'] in ['Critical', 'High']]
        return len(critical_high) > 0
    
    def get_statistics(self, findings: List[Dict]) -> Dict:
        """Get statistics about static findings"""
        if not findings:
            return {
                'total': 0,
                'critical': 0,
                'high': 0,
                'medium': 0,
                'low': 0,
                'types': {}
            }
        
        stats = {
            'total': len(findings),
            'critical': sum(1 for f in findings if f['severity'] == 'Critical'),
            'high': sum(1 for f in findings if f['severity'] == 'High'),
            'medium': sum(1 for f in findings if f['severity'] == 'Medium'),
            'low': sum(1 for f in findings if f['severity'] == 'Low'),
            'types': {}
        }
        
        # Count by type
        for finding in findings:
            vuln_type = finding['type']
            stats['types'][vuln_type] = stats['types'].get(vuln_type, 0) + 1
        
        return stats
