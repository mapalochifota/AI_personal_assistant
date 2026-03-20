import ast
import operator
from tools.base_tool import BaseTool

class CalculatorTool(BaseTool):

    @property
    def name(self) -> str:
        return "calculator"

    @property
    def description(self) -> str:
        return "Evaluates mathematical expressions like 2 + 2 or 15% of 340."

    def execute(self, args: dict) -> str:
        expression = args.get("expression", "").strip()

        allowed_operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.Mod: operator.mod,
            ast.USub: operator.neg,
        }

        def safe_eval(node):
            if isinstance(node, ast.Constant):
                return node.n
            elif isinstance(node, ast.BinOp):
                op = allowed_operators.get(type(node.op))
                if op is None:
                    raise ValueError("Unsupported operator")
                return op(safe_eval(node.left), safe_eval(node.right))
            elif isinstance(node, ast.UnaryOp):
                op = allowed_operators.get(type(node.op))
                return op(safe_eval(node.operand))
            else:
                raise ValueError("Unsupported expression")

        try:
            tree = ast.parse(expression, mode='eval')
            result = safe_eval(tree.body)

            print(f"\n  [Calculator]")
            print(f"  Expression : {expression}")
            print(f"  Result     : {result}\n")

            return f"{expression} = {result}"

        except Exception as e:
            return f"Error calculating '{expression}': {str(e)}"

    def get_declaration(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The math expression to evaluate e.g. 100 * 0.15"
                    }
                },
                "required": ["expression"]
            }
        }