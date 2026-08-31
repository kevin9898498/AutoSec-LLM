from __future__ import annotations

import ast
from .models import SyntaxCheck


def check_python_syntax(code: str) -> SyntaxCheck:
    try:
        tree = ast.parse(code)
        compile(tree, "generated.py", "exec")
        return SyntaxCheck(valid=True)
    except (SyntaxError, ValueError, TypeError) as exc:
        return SyntaxCheck(valid=False, error=f"{exc.__class__.__name__}: {exc}")
