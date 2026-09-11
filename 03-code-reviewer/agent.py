import keyword

from dotenv import load_dotenv
from pydantic_ai import Agent
from models import CodeReview

load_dotenv()


agent = Agent(
    "google:gemini-3.6-flash",
    instructions="""You are a senior Python code reviewer. You will be given the source of a single Python function, with each line prefixed by its line number.

Review it for:
- Bugs: logic errors, unhandled edge cases (empty input, None, division by zero), mutable default arguments
- Style: PEP 8 formatting and naming
- Type hints: missing or incorrect parameter and return annotations
- Error handling: bare `except`, swallowed exceptions, missing input validation
- Readability: unclear names, magic numbers, deep nesting, missing docstring

Always call check_naming_convention with the function's name. If it fails, report it as a warning.

For each issue, set line_reference to the line number it's on (e.g. "line 4"), or leave it empty if the issue is about the whole function.

Severity:
- critical: a bug that gives wrong results or crashes at runtime
- warning: works, but is fragile, unsafe, or clearly against Python conventions
- suggestion: optional polish that would improve readability or maintainability

Overall quality:
- good: no critical issues or warnings
- needs_improvement: no critical issues, but has warnings worth fixing
- poor: has at least one critical issue

If the function is clean, return an empty issues list — don't invent problems.

Each suggestion should be one concrete, actionable sentence (e.g. "Add a return type hint: -> float").
""",
    output_type=CodeReview,
    # Build the Gemini client on first run, not at import, so tests need no API key
    defer_model_check=True,
)


@agent.tool_plain
def check_naming_convention(name: str) -> dict:
    """Check whether a function name follows Python's snake_case convention (PEP 8).

    Args:
        name: The function name only, without `def`, parentheses, or arguments.
    """
    if not name.isidentifier() or keyword.iskeyword(name):
        return {"passes": False, "reason": f"'{name}' is not a valid Python name."}
    if name != name.lower():
        return {
            "passes": False,
            "reason": f"'{name}' contains uppercase letters. Function names should be lowercase words separated by underscores.",
        }
    if "__" in name.strip("_"):
        return {
            "passes": False,
            "reason": f"'{name}' has consecutive underscores between words. Use a single underscore.",
        }
    return {"passes": True, "reason": f"'{name}' follows snake_case."}


def number_lines(source: str) -> str:
    """Prefix each line with its number so the model can cite lines accurately."""
    lines = source.strip("\n").splitlines()
    return "\n".join(f"{i:>3} | {line}" for i, line in enumerate(lines, start=1))
