import ast
import logging
from typing import List, Set, Dict
from vulnora.models.issue import IssueCandidate

logger = logging.getLogger("vulnora.analyzers.taint")

SOURCES = {
    'input', 'request.args.get', 'request.form.get', 'request.values.get', 'request.json',
    'sys.argv', 'os.environ.get'
}

SINKS = {
    'eval': 'Code Injection',
    'exec': 'Code Injection',
    'os.system': 'Command Injection',
    'subprocess.call': 'Command Injection',
    'subprocess.Popen': 'Command Injection',
    'sqlite3.execute': 'SQL Injection',
    'cursor.execute': 'SQL Injection'
}

class TaintVisitor(ast.NodeVisitor):
    def __init__(self, file_path: str, content: str):
        self.file_path = file_path
        self.content = content
        self.issues: List[IssueCandidate] = []
        self.tainted_vars: Set[str] = set()

    def visit_Assign(self, node: ast.Assign):
        # Check if assignment source is a taint source
        is_tainted = False
        if isinstance(node.value, ast.Call):
            if isinstance(node.value.func, ast.Name) and node.value.func.id in SOURCES:
                is_tainted = True
            elif isinstance(node.value.func, ast.Attribute):
                attr_name = f"{node.value.func.value.id}.{node.value.func.attr}" if isinstance(node.value.func.value, ast.Name) else node.value.func.attr
                if attr_name in SOURCES:
                    is_tainted = True
        
        if is_tainted:
            for target in node.targets:
                if isinstance(target, ast.Name):
                    self.tainted_vars.add(target.id)
        
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        # Check if call is a sink
        sink_type = None
        if isinstance(node.func, ast.Name) and node.func.id in SINKS:
            sink_type = SINKS[node.func.id]
        elif isinstance(node.func, ast.Attribute):
            # Simple attribute check (e.g. os.system)
            attr_name = node.func.attr
            # Ideally we check the full path, but for now simple check
            for sink, type_ in SINKS.items():
                if sink.endswith(f".{attr_name}"):
                    sink_type = type_
                    break
        
        if sink_type:
            # Check if arguments are tainted
            for arg in node.args:
                if isinstance(arg, ast.Name) and arg.id in self.tainted_vars:
                    self._add_issue(node, "PY-TAINT-001", sink_type, "High", f"Tainted variable '{arg.id}' flows into dangerous sink.")
                elif isinstance(arg, ast.BinOp): # Check for f-strings or concatenation involving tainted vars
                    # Simplified check for binary ops
                    pass 

        self.generic_visit(node)

    def _add_issue(self, node: ast.AST, rule_id: str, name: str, severity: str, description: str):
        self.issues.append(IssueCandidate(
            file_path=self.file_path,
            line_number=node.lineno,
            column=node.col_offset,
            rule_id=rule_id,
            vulnerability_type=name,
            severity=severity,
            description=description,
            confidence="Medium",
            snippet=self.content.splitlines()[node.lineno - 1].strip(),
            suggested_fix="Sanitize input before using in sensitive functions."
        ))

class TaintAnalyzer:
    def scan_file(self, file_path: str, content: str) -> List[IssueCandidate]:
        if not file_path.endswith('.py'):
            return []
            
        try:
            tree = ast.parse(content)
            visitor = TaintVisitor(file_path, content)
            visitor.visit(tree)
            return visitor.issues
        except Exception as e:
            logger.error(f"Error analyzing taint in {file_path}: {e}")
            return []
