import ast
from typing import List, Dict, Set

class TaintAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.issues = []
        self.tainted_vars: Set[str] = set()
        self.sources = {'input', 'request.GET', 'request.POST', 'request.args', 'request.form', 'sys.argv'}
        self.sinks = {'eval', 'exec', 'subprocess.Popen', 'os.system', 'os.popen', 'sqlite3.connect', 'cursor.execute'}
        self.current_file = ""

    def scan_file(self, file_path: str, content: str) -> List[Dict]:
        self.issues = []
        self.tainted_vars = set()
        self.current_file = file_path
        try:
            tree = ast.parse(content)
            self.visit(tree)
        except SyntaxError:
            pass # Skip files with syntax errors
        return self.issues

    def visit_Assign(self, node):
        # Check if assignment source is tainted
        is_tainted = False
        if isinstance(node.value, ast.Call):
            if isinstance(node.value.func, ast.Name) and node.value.func.id in self.sources:
                is_tainted = True
            elif isinstance(node.value.func, ast.Attribute) and node.value.func.attr in self.sources: # Simplified check
                 is_tainted = True
        
        # If right side is a variable that is already tainted
        elif isinstance(node.value, ast.Name) and node.value.id in self.tainted_vars:
            is_tainted = True
            
        # If right side is a BinOp involving tainted var (e.g. x + "str")
        elif isinstance(node.value, ast.BinOp):
             if (isinstance(node.value.left, ast.Name) and node.value.left.id in self.tainted_vars) or \
                (isinstance(node.value.right, ast.Name) and node.value.right.id in self.tainted_vars):
                 is_tainted = True

        if is_tainted:
            for target in node.targets:
                if isinstance(target, ast.Name):
                    self.tainted_vars.add(target.id)
        
        self.generic_visit(node)

    def visit_Call(self, node):
        # Check if call is a sink
        sink_name = None
        if isinstance(node.func, ast.Name):
            if node.func.id in self.sinks:
                sink_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
             # Check for object.method calls like cursor.execute
             full_name = f"{node.func.value.id if isinstance(node.func.value, ast.Name) else 'obj'}.{node.func.attr}"
             if node.func.attr in self.sinks or full_name in self.sinks:
                 sink_name = node.func.attr

        if sink_name:
            # Check if any argument is tainted
            for arg in node.args:
                if isinstance(arg, ast.Name) and arg.id in self.tainted_vars:
                    self.issues.append({
                        "file_path": self.current_file,
                        "line_number": node.lineno,
                        "column": node.col_offset,
                        "rule_id": "TAINT-001",
                        "vulnerability_type": "Taint Flow",
                        "severity": "High",
                        "description": f"Tainted variable '{arg.id}' flows into sink '{sink_name}'",
                        "snippet": f"Call to {sink_name}",
                        "suggested_fix": "Sanitize input before using it in sensitive functions."
                    })
        
        self.generic_visit(node)
