import os
from pathlib import Path
import ast
import operator
import re

from ddgs import DDGS


# -------------------------
# Configuration
# -------------------------

VAULT_PATH = Path(
    os.getenv("OBSIDIAN_VAULT_PATH", "Obsidian_Notes")
).expanduser()

OUTPUT_DIR = VAULT_PATH / "AI Generated"


# -------------------------
# Calculator
# -------------------------

# Only allow basic arithmetic operations.
_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _evaluate_math(node):
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return node.value

    if isinstance(node, ast.BinOp) and type(node.op) in _OPERATORS:
        left = _evaluate_math(node.left)
        right = _evaluate_math(node.right)

        # Prevent excessively large calculations.
        if isinstance(node.op, ast.Pow):
            if abs(right) > 100 or abs(left) > 1_000_000:
                raise ValueError("Exponent too large.")

        result = _OPERATORS[type(node.op)](left, right)

        if isinstance(result, (int, float)) and abs(result) > 1e100:
            raise ValueError("Result too large.")

        return result

    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPERATORS:
        return _OPERATORS[type(node.op)](_evaluate_math(node.operand))

    raise ValueError("Unsupported mathematical expression.")


def calculator(expression):
    try:
        tree = ast.parse(expression, mode="eval")
        return str(_evaluate_math(tree.body))
    except Exception:
        return "I couldn't calculate that expression."


# -------------------------
# Web search
# -------------------------

def web_search(query):
    try:
        results = DDGS().text(query, max_results=3)
        output = []

        for result in results:
            output.append(
                f"Title: {result.get('title', 'Untitled')}\n"
                f"URL: {result.get('href', '')}\n"
                f"Summary: {result.get('body', '')}"
            )

        return "\n\n".join(output) or "No search results found."

    except Exception as e:
        return f"Search failed: {e}"


# -------------------------
# Obsidian Markdown writer
# -------------------------

def write_markdown(title, content):
    try:
        if not VAULT_PATH.is_dir():
            return "Error: Obsidian vault not found. Check VAULT_PATH."

        if not title.strip() or not content.strip():
            return "Error: Both title and content are required."

        filename = re.sub(
            r'[<>:"/\\|?*\x00-\x1f]', "", title
        )
        filename = re.sub(r"\s+", " ", filename).strip().rstrip(". ")

        if not filename:
            return "Error: Invalid document title."

        reserved = {
            "CON", "PRN", "AUX", "NUL",
            *(f"COM{i}" for i in range(1, 10)),
            *(f"LPT{i}" for i in range(1, 10)),
        }

        if filename.upper() in reserved:
            filename = f"Note - {filename}"

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        # Avoid overwriting existing notes.
        path = OUTPUT_DIR / f"{filename}.md"
        counter = 2

        while path.exists():
            path = OUTPUT_DIR / f"{filename} ({counter}).md"
            counter += 1

        markdown = content.strip()

        if not re.match(r"^#\s+", markdown):
            markdown = f"# {title.strip()}\n\n{markdown}"

        path.write_text(markdown + "\n", encoding="utf-8")

        return f"Document saved successfully: {path}"

    except OSError as e:
        return f"Could not save the document: {e}"


# -------------------------
# Tool schemas for Ollama
# -------------------------

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Calculate a mathematical expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "For example, 25 * 4."
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": (
                "Search the internet for information. "
                "Use actual returned URLs when citing research."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query."
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_markdown",
            "description": (
                "Save a complete Markdown document to the user's "
            	"Obsidian vault. Use whenever the user asks to "
            	"create, write, or save a document."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "content": {"type": "string"}
                },
                "required": ["title", "content"]
            }
        }
    }
]


# -------------------------
# Tool dispatcher
# -------------------------

def run_tool(name, arguments):
    try:
        if name == "calculator":
            return calculator(arguments["expression"])

        elif name == "web_search":
            return web_search(arguments["query"])

        elif name == "write_markdown":
            return write_markdown(
                arguments["title"],
                arguments["content"]
            )

        return f"Unknown tool: {name}"

    except Exception as e:
        return f"Tool error ({name}): {e}"
