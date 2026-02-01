"""
Safe evaluator for math expressions used by the calculator.
"""

import ast
import operator
import math

# --- Safe evaluator ---------------------------------------------------------

ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

# Allowed functions for safe calls
ALLOWED_FUNCTIONS = {
    'sqrt': math.sqrt,
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'log': math.log,  # log(x) or log(x, base)
    'abs': abs,
}


def safe_eval(expr: str) -> float:
    """Evaluate a math expression safely using ast.

    Supports: + - * / % ** unary +/- and parentheses.
    """
    # replace friendly symbols
    expr = expr.replace("×", "*").replace("÷", "/").replace('^', '**')

    try:
        node = ast.parse(expr, mode="eval")
    except Exception as exc:
        raise ValueError("Invalid expression") from exc

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Constant):  # python 3.8+
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Invalid constant")
        NumNode = getattr(ast, 'Num', None)
        if NumNode is not None and isinstance(node, NumNode):  # older nodes
            return node.n
        if isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            op_type = type(node.op)
            if op_type in ALLOWED_OPERATORS:
                try:
                    return ALLOWED_OPERATORS[op_type](left, right)
                except ZeroDivisionError:
                    raise ValueError("Division by zero")
            raise ValueError("Unsupported operator")
        if isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            op_type = type(node.op)
            if op_type in ALLOWED_OPERATORS:
                return ALLOWED_OPERATORS[op_type](operand)
            raise ValueError("Unsupported unary operator")
        # function calls like sqrt(9), sin(0)
        if isinstance(node, ast.Call):
            # only allow simple name calls: e.g., sqrt(x)
            if isinstance(node.func, ast.Name) and node.func.id in ALLOWED_FUNCTIONS:
                func = ALLOWED_FUNCTIONS[node.func.id]
                args = [_eval(a) for a in node.args]
                try:
                    return func(*args)
                except TypeError:
                    raise ValueError("Invalid function arguments")
            raise ValueError("Unsupported function call")
        raise ValueError(f"Unsupported expression: {type(node)}")

    result = _eval(node)
    return result
