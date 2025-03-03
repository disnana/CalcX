import math
from fractions import Fraction

def calc_expr(expr: str) -> str:
    expr = expr.replace("^", "")
    if any(token in expr for token in ['pi', 'e', 'sin', 'cos', 'tan', 'log', 'sqrt']):
        safe_dict = {
            "pi": math.pi,
            "e": math.e,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "sqrt": math.sqrt,
            "log": math.log,
            "log10": math.log10
        }
        try:
            result = eval(expr, {"__builtins__": {}}, safe_dict)
            return str(round(result, 12))
        except Exception:
            return "Error"
    else:
        try:
            result = eval(expr, {"__builtins__": {}}, {})
            frac = Fraction(str(result))
            if frac.denominator == 1:
                return str(frac.numerator)
            else:
                return f"{frac.numerator}/{frac.denominator}"
        except Exception:
            return "Error"
