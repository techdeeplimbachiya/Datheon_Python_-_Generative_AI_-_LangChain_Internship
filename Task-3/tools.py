import ast
import json
import math
import operator
from pathlib import Path

from ddgs import DDGS
from langchain.tools import tool


BASE_DIR = Path(__file__).resolve().parent
DOCUMENTS_DIR = BASE_DIR / "documents"

BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def check_number(value):
    if type(value) not in (int, float):
        raise ValueError("Only real numbers are supported.")

    if not math.isfinite(value):
        raise ValueError("Number must be finite.")

    if abs(value) > 1e50:
        raise ValueError("Number exceeds the supported limit.")

    return value


def evaluate_node(node):
    if isinstance(node, ast.Constant):
        return check_number(node.value)

    if isinstance(node, ast.UnaryOp):
        operation = UNARY_OPERATORS.get(type(node.op))

        if operation is None:
            raise ValueError("Unsupported unary operator.")

        return check_number(operation(evaluate_node(node.operand)))

    if isinstance(node, ast.BinOp):
        operation = BINARY_OPERATORS.get(type(node.op))

        if operation is None:
            raise ValueError("Unsupported arithmetic operator.")

        left = evaluate_node(node.left)
        right = evaluate_node(node.right)

        if isinstance(node.op, ast.Pow) and abs(right) > 10:
            raise ValueError("Exponent must be between -10 and 10.")

        return check_number(operation(left, right))

    raise ValueError(
        "Use numbers, parentheses, and + - * / // % ** only."
    )


@tool
def calculator(expression: str) -> str:
    """Calculate basic arithmetic. Example: (12 * 19.95) + 15."""
    try:
        if len(expression) > 200:
            return "Calculation error: expression is too long."

        tree = ast.parse(expression, mode="eval")

        if sum(1 for _ in ast.walk(tree)) > 80:
            return "Calculation error: expression is too complex."

        result = evaluate_node(tree.body)

        return json.dumps({
            "expression": expression,
            "result": result,
        })

    except (
        SyntaxError,
        ValueError,
        TypeError,
        ZeroDivisionError,
        OverflowError,
        RecursionError,
    ) as exc:
        return f"Calculation error: {exc}"


@tool
def web_search(query: str) -> str:
    """Search DuckDuckGo for current public information and source URLs."""
    try:
        query = query.strip()

        if not query:
            return "Search error: query cannot be empty."

        results = list(
            DDGS(timeout=20).text(
                query,
                backend="duckduckgo",
                max_results=5,
            )
        )

        if not results:
            return "No search results found."

        sources = [
            {
                "title": item.get("title", ""),
                "url": item.get("href", ""),
                "snippet": item.get("body", ""),
            }
            for item in results
        ]

        return json.dumps(sources, ensure_ascii=False, indent=2)

    except Exception as exc:
        return f"Web search failed: {type(exc).__name__}: {exc}"


@tool
def read_local_file(filename: str) -> str:
    """Read a UTF-8 file relative to the project's documents folder."""
    try:
        relative_path = Path(filename)

        if relative_path.is_absolute():
            return "Access denied: provide a relative filename."

        root = DOCUMENTS_DIR.resolve()
        requested = (root / relative_path).resolve()

        if not requested.is_relative_to(root):
            return "Access denied: file must be inside documents."

        if not requested.is_file():
            return f"File not found: {filename}"

        # Read at most 200 KB plus one byte to detect oversized files.
        with requested.open("rb") as file:
            data = file.read(200_001)

        if len(data) > 200_000:
            return "File too large: maximum supported size is 200 KB."

        return data.decode("utf-8")

    except (OSError, UnicodeDecodeError, ValueError) as exc:
        return f"File read failed: {exc}"