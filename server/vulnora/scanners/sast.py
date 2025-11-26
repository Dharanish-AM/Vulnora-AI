import ast
import logging
from typing import List, Dict, Any
from vulnora.models.issue import IssueCandidate

logger = logging.getLogger("vulnora.scanners.sast")

class PythonASTVisitor(ast.NodeVisitor):
    def __init__(self, file_path: str, content: str):
        self.file_path = file_path
        self.content = content
        self.issues: List[IssueCandidate] = []

    def _add_issue(self, node: ast.AST, rule_id: str, name: str, severity: str, description: str, fix: str = None, fix_theory: str = None):
        self.issues.append(IssueCandidate(
            file_path=self.file_path,
            line_number=node.lineno,
            column=node.col_offset,
            rule_id=rule_id,
            vulnerability_type=name,
            severity=severity,
            description=description,
            confidence="High",
            snippet=self.content.splitlines()[node.lineno - 1].strip(),
            suggested_fix=fix if fix else "Review the code and replace insecure functions.",
            fix_theory=fix_theory
        ))

    def visit_Call(self, node: ast.Call):
        # Check for eval()
        if isinstance(node.func, ast.Name) and node.func.id == 'eval':
            self._add_issue(node, "PY-AST-001", "Eval Usage", "Critical", "Use of eval() is dangerous and can lead to RCE.", 
                            fix="ast.literal_eval(...)",
                            fix_theory="The eval() function executes a string as code, which can be exploited to run malicious code. ast.literal_eval() safely evaluates a string containing a Python literal or container display.")
        
        # Check for subprocess with shell=True
        if isinstance(node.func, ast.Attribute) and node.func.attr in ['Popen', 'run', 'call']:
            # Check keywords
            for keyword in node.keywords:
                if keyword.arg == 'shell' and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                     # Generate fix: replace shell=True with shell=False
                     original_line = self.content.splitlines()[node.lineno - 1].strip()
                     fixed_line = original_line.replace("shell=True", "shell=False")
                     self._add_issue(node, "PY-AST-002", "Command Injection", "Critical", "subprocess call with shell=True is vulnerable to command injection.",
                                     fix=fixed_line,
                                     fix_theory="Using shell=True invokes a system shell, allowing attackers to execute arbitrary commands via shell metacharacters. Setting shell=False (default) executes the command directly, preventing injection.")
        
        self.generic_visit(node)

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            if alias.name == 'telnetlib':
                self._add_issue(node, "PY-AST-003", "Insecure Module", "High", "telnetlib is insecure and should not be used.")
        self.generic_visit(node)

class SASTScanner:
    def scan_file(self, file_path: str, content: str) -> List[IssueCandidate]:
        if not file_path.endswith('.py'):
            return []
            
        try:
            tree = ast.parse(content)
            visitor = PythonASTVisitor(file_path, content)
            visitor.visit(tree)
            return visitor.issues
        except SyntaxError:
            logger.warning(f"Syntax error parsing {file_path}")
            return []
        except Exception as e:
            logger.error(f"Error scanning {file_path}: {e}")
            return []
